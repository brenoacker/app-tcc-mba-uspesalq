from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, Numeric,
                        String, create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

from infrastructure.api.database import Base, create_tables, get_session

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
    user_id = Column(String, nullable=False)
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
    user_id = Column(String, nullable=False)
    cart_id = Column(String, nullable=False)
    offer_id = Column(Integer, nullable=True)
    type = Column(String, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

@pytest.fixture
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture
def session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def test_get_session(mocker, session):
    with patch('infrastructure.api.database.SessionLocal', return_value=session):
        mock_close = mocker.patch.object(session, 'close', autospec=True)
        gen = get_session()
        db = next(gen)
        assert db == session
        next(gen, None)
        mock_close.assert_called_once()

def test_get_session_exception(session):
    with patch('infrastructure.api.database.SessionLocal', return_value=session):
        gen = get_session()
        db = next(gen)
        assert db == session
        with pytest.raises(StopIteration):
            next(gen)

def test_create_tables(engine):
    with patch('infrastructure.api.database.engine', engine):
        Base.metadata.create_all(bind=engine, tables=[UserModel.__table__, OfferModel.__table__, CartModel.__table__])
        Base.metadata.create_all(bind=engine, tables=[OrderModel.__table__])
        # Verifica se as tabelas foram criadas
        assert Base.metadata.tables != {}

        assert 'tb_users' in Base.metadata.tables
        assert 'tb_carts' in Base.metadata.tables
        assert 'tb_offers' in Base.metadata.tables
        assert 'tb_orders' in Base.metadata.tables

