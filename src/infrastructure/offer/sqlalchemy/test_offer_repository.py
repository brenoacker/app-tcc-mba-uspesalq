from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from infrastructure.offer.sqlalchemy.offer_model import OfferModel
from infrastructure.offer.sqlalchemy.offer_repository import OfferRepository


@pytest.fixture
def session():
    return MagicMock()

@pytest.fixture
def offer_repository(session):
    return OfferRepository(session)

@pytest.mark.asyncio
async def test_add_offer(offer_repository, session):
    offer = Offer(
        id=1,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
        discount_type=OfferType.PERCENTAGE,
        discount_value=10.0
    )
    
    # Mock the session's async methods
    session.commit = async_return(None)
    session.refresh = async_return(None)

    added_offer = await offer_repository.add_offer(offer)

    # Check that the session methods were called
    assert session.add.called
    assert session.commit.called
    assert session.refresh.called
    assert added_offer.id == offer.id
    assert added_offer.start_date == offer.start_date
    assert added_offer.end_date == offer.end_date
    assert added_offer.discount_type == offer.discount_type
    assert added_offer.discount_value == offer.discount_value

@pytest.mark.asyncio
async def test_find_offer(offer_repository, session):
    offer_id = 1
    offer_model = OfferModel(
        id=offer_id,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
        discount_type=OfferType.PERCENTAGE,
        discount_value=10.0
    )
    
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = offer_model

    found_offer = await offer_repository.find_offer(offer_id)

    assert found_offer.id == offer_id
    assert found_offer.start_date == offer_model.start_date
    assert found_offer.end_date == offer_model.end_date
    assert found_offer.discount_type == offer_model.discount_type
    assert found_offer.discount_value == offer_model.discount_value

@pytest.mark.asyncio
async def test_find_offer_not_found(offer_repository, session):
    offer_id = 1
    
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = None

    found_offer = await offer_repository.find_offer(offer_id)

    assert found_offer is None

@pytest.mark.asyncio
async def test_list_offers(offer_repository, session):
    offer_model_1 = OfferModel(
        id=1,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
        discount_type=OfferType.PERCENTAGE,
        discount_value=10.0
    )
    offer_model_2 = OfferModel(
        id=2,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
        discount_type=OfferType.AMOUNT,
        discount_value=20.0
    )
    
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.all.return_value = [offer_model_1, offer_model_2]

    offers = await offer_repository.list_offers()

    assert len(offers) == 2
    assert offers[0].id == offer_model_1.id
    assert offers[1].id == offer_model_2.id

@pytest.mark.asyncio
async def test_list_offers_empty(offer_repository, session):
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.all.return_value = []

    offers = await offer_repository.list_offers()

    assert offers is None

@pytest.mark.asyncio
async def test_remove_offer(offer_repository, session):
    offer_id = 1
    
    # Create a mock offer model
    offer_model = OfferModel(
        id=offer_id,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
        discount_type=OfferType.PERCENTAGE,
        discount_value=10.0
    )
    
    # Mock all the session methods we need
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = offer_model
    session.delete = async_return(None)
    session.commit = async_return(None)

    await offer_repository.remove_offer(offer_id)

    # Verify the methods were called
    assert session.execute.called
    assert session.delete.called
    assert session.commit.called

@pytest.mark.asyncio
async def test_remove_all_offers_success(offer_repository, session):
    # Mock the session methods
    session.execute = async_return(MagicMock())
    session.commit = async_return(None)
    
    # Act
    result = await offer_repository.remove_all_offers()

    # Assert
    assert session.execute.called
    assert session.commit.called
    assert result is None