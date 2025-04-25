from uuid import uuid4

import pytest
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, Numeric,
                        String, create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

from domain.user.user_gender_enum import UserGender
from infrastructure.api.database import Base
from infrastructure.cart.sqlalchemy.cart_model import CartModel
from infrastructure.order.sqlalchemy.order_model import (OrderStatusType,
                                                         OrderTType)
from infrastructure.user.sqlalchemy.user_model import UserGenderType

from domain.__seedwork.test_utils import run_async, async_return, async_side_effect

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
    


def created_user(session):
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

    return user

@pytest.mark.asyncio
async def test_cart_model_mapping(session):
    cart_id = str(uuid4())
    user_id = created_user(session).id
    session.commit()

    cart = CartModel(
        id=cart_id,
        user_id=user_id,
        total_price=100.0
    )
    session.add(cart)
    session.commit()

    retrieved_cart = session.query(CartModel).filter_by(id=cart_id).first()
    assert retrieved_cart is not None
    assert retrieved_cart.id == cart_id
    assert retrieved_cart.user_id == user_id
    assert retrieved_cart.total_price == 100.0