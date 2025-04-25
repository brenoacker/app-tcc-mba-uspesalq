from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.offer.offer_type_enum import OfferType
from infrastructure.api.database import Base
from infrastructure.api.test_database import CartModel, OrderModel, UserModel
from infrastructure.offer.sqlalchemy.offer_model import (OfferDiscountType,
                                                         OfferModel)


@pytest.fixture
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture
def session(engine):
    Base.metadata.create_all(bind=engine, tables=[OfferModel.__table__])
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.mark.asyncio
async def test_offer_model_mapping(session):
    offer = OfferModel(
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
        discount_type=OfferType.PERCENTAGE,
        discount_value=10.0
    )
    session.add(offer)
    session.commit()

    retrieved_offer = session.query(OfferModel).filter_by(id=offer.id).first()
    assert retrieved_offer is not None
    assert retrieved_offer.start_date == datetime(2023, 1, 1)
    assert retrieved_offer.end_date == datetime(2023, 12, 31)
    assert retrieved_offer.discount_type == OfferType.PERCENTAGE
    assert retrieved_offer.discount_value == 10.0

@pytest.mark.asyncio
async def test_offer_discount_type():
    offer_discount_type = OfferDiscountType()
    assert offer_discount_type.process_bind_param(OfferType.PERCENTAGE, None) == 'percentage'
    assert offer_discount_type.process_result_value('percentage', None) == OfferType.PERCENTAGE

@pytest.mark.asyncio
async def test_offer_discount_type_none():
    offer_discount_type = OfferDiscountType()
    assert offer_discount_type.process_bind_param(None, None) is None
    assert offer_discount_type.process_result_value(None, None) is None