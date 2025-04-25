from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, Numeric,
                        String, create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from infrastructure.api.database import Base
from infrastructure.payment.sqlalchemy.payment_model import (
    PaymentCardGatewayType, PaymentMethodType, PaymentModel, PaymentStatusType)

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "tb_users"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)

class CartModel(Base):
    __tablename__ = "tb_carts"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("tb_users.id"), nullable=False)
    total_price = Column(Float, nullable=False)

class OfferModel(Base):
    __tablename__ = "tb_offers"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    discount_type = Column(String, nullable=False)
    discount_value = Column(Float, nullable=False)

class OrderModel(Base):
    __tablename__ = "tb_orders"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("tb_users.id"), nullable=False)
    cart_id = Column(String, ForeignKey("tb_carts.id", ondelete="CASCADE"), nullable=False)
    offer_id = Column(Integer, ForeignKey("tb_offers.id"), nullable=True)
    type = Column(String, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class PaymentModel(Base):
    __tablename__ = 'tb_payments'
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('tb_users.id'), nullable=False)
    order_id = Column(String, ForeignKey('tb_orders.id'), nullable=False)
    payment_method = Column(PaymentMethodType, nullable=True)
    payment_card_gateway = Column(PaymentCardGatewayType, nullable=True)
    status = Column(PaymentStatusType, nullable=False)

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def create_user(session):
    user_id = str(uuid4())
    user = UserModel(
        id=user_id,
        name="John Doe",
        email="fds@gmail.com",
        age=25,
        gender="male",
        phone_number="123456789",
        password="password"
    )
    session.add(user)
    session.commit()

    return user_id

def create_cart(session, user_id):
    cart_id = str(uuid4())
    cart = CartModel(
        id=cart_id,
        user_id=user_id,
        total_price=100.0
    )
    session.add(cart)
    session.commit()

    return cart.id

def create_order(session, user_id, cart_id):
    order_id = str(uuid4())
    order = OrderModel(
        id=order_id,
        user_id=user_id,
        cart_id=cart_id,
        offer_id=1,
        type="delivery",
        total_price=100.0,
        status="PENDING",
        created_at=datetime.now(),
        updated_at=datetime.now() + timedelta(days=1)
    )
    session.add(order)
    session.commit()

    return order_id


@pytest.mark.asyncio
async def test_payment_model_mapping(session):
    payment_id = str(uuid4())
    user_id = create_user(session)
    cart_id = create_cart(session, user_id)
    order_id = create_order(session, user_id, cart_id)

    payment = PaymentModel(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method='card',
        payment_card_gateway="adyen",
        status="PAID"
    )
    session.add(payment)
    session.commit()

    retrieved_payment = session.query(PaymentModel).filter_by(id=payment_id).first()
    assert retrieved_payment is not None
    assert retrieved_payment.id == payment_id
    assert retrieved_payment.user_id == user_id
    assert retrieved_payment.order_id == order_id
    assert retrieved_payment.payment_method == PaymentMethod.CARD
    assert retrieved_payment.payment_card_gateway == PaymentCardGateway.ADYEN
    assert retrieved_payment.status == PaymentStatus.PAID

@pytest.mark.asyncio
async def test_payment_method_type():
    payment_method_type = PaymentMethodType()
    
    # Teste com valor do tipo PaymentMethod
    assert payment_method_type.process_bind_param(PaymentMethod.CARD, None) == 'card'
    
    # Teste com valor do tipo string
    assert payment_method_type.process_bind_param('card', None) == 'card'
    
    # Teste com valor None
    assert payment_method_type.process_bind_param(None, None) is None
    
    # Teste com valor do tipo string
    assert payment_method_type.process_result_value('card', None) == PaymentMethod.CARD
    
    # Teste com valor None
    assert payment_method_type.process_result_value(None, None) is None

@pytest.mark.asyncio
async def test_payment_card_gateway_type():
    payment_card_gateway_type = PaymentCardGatewayType()
    
    # Teste com valor do tipo PaymentCardGateway
    assert payment_card_gateway_type.process_bind_param(PaymentCardGateway.ADYEN, None) == 'adyen'
    
    # Teste com valor do tipo string
    assert payment_card_gateway_type.process_bind_param('adyen', None) == 'adyen'
    
    # Teste com valor None
    assert payment_card_gateway_type.process_bind_param(None, None) is None
    
    # Teste com valor do tipo string
    assert payment_card_gateway_type.process_result_value('adyen', None) == PaymentCardGateway.ADYEN
    
    # Teste com valor None
    assert payment_card_gateway_type.process_result_value(None, None) is None

@pytest.mark.asyncio
async def test_payment_status_type():
    payment_status_type = PaymentStatusType()
    
    # Teste com valor do tipo PaymentStatus
    assert payment_status_type.process_bind_param(PaymentStatus.PAID, None) == 'PAID'
    
    # Teste com valor do tipo string
    assert payment_status_type.process_bind_param('PAID', None) == 'PAID'
    
    # Teste com valor None
    assert payment_status_type.process_bind_param(None, None) is None
    
    # Teste com valor do tipo string
    assert payment_status_type.process_result_value('PAID', None) == PaymentStatus.PAID
    
    # Teste com valor None
    assert payment_status_type.process_result_value(None, None) is None