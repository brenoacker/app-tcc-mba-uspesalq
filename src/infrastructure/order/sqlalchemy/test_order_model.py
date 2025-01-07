from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, Numeric,
                        String, create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from infrastructure.order.sqlalchemy.order_model import (OrderModel,
                                                         OrderStatusType,
                                                         OrderTType)

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
    type = Column(OrderTType, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(OrderStatusType, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
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

def test_order_model_mapping(session):
    datetime_now = datetime.now()

    order = OrderModel(
        id=str(uuid4()),
        user_id=str(uuid4()),
        cart_id=str(uuid4()),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime_now,
        updated_at=datetime_now
    )
    session.add(order)
    session.commit()

    retrieved_order = session.query(OrderModel).filter_by(id=order.id).first()
    assert retrieved_order is not None
    assert retrieved_order.id == order.id
    assert retrieved_order.user_id == order.user_id
    assert retrieved_order.cart_id == order.cart_id
    assert retrieved_order.offer_id == 1
    assert retrieved_order.type == OrderType.DELIVERY
    assert retrieved_order.total_price == 100.00
    assert retrieved_order.status == OrderStatus.PENDING
    assert retrieved_order.created_at == datetime_now
    assert retrieved_order.updated_at == datetime_now

def test_order_status_type(session):
    order_status_type = OrderStatusType()
    order_status = OrderStatus.PENDING

    assert order_status_type.process_bind_param(order_status, None) == order_status.value
    assert order_status_type.process_result_value(order_status.value, None) == order_status

def test_order_status_type_none(session):
    order_status_type = OrderStatusType()
    order_status = None

    assert order_status_type.process_bind_param(order_status, None) == order_status
    assert order_status_type.process_result_value(order_status, None) == order_status

def test_order_t_type(session):
    order_t_type = OrderTType()
    order_type = OrderType.DELIVERY

    assert order_t_type.process_bind_param(order_type, None) == order_type.value
    assert order_t_type.process_result_value(order_type.value, None) == order_type

def test_order_t_type_none(session):
    order_t_type = OrderTType()
    order_type = None

    assert order_t_type.process_bind_param(order_type, None) == order_type
    assert order_t_type.process_result_value(order_type, None) == order_type