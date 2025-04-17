import random
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from usecases.offer.list_offers.list_offers_dto import (ListOffersOutputDto,
                                                        OfferDto)
from usecases.offer.list_offers.list_offers_usecase import ListOffersUseCase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def list_offers_usecase(offer_repository):
    return ListOffersUseCase(offer_repository)

@pytest.mark.asyncio
async def test_list_offers_success(list_offers_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.list_offers = async_return([offer])
    
    output_dto = await list_offers_usecase.execute()
    
    assert len(output_dto.offers) == 1
    assert output_dto.offers[0].id == offer_id
    assert output_dto.offers[0].discount_type == OfferType.PERCENTAGE
    assert output_dto.offers[0].discount_value == 20.0
    offer_repository.list_offers.await_count == 1

@pytest.mark.asyncio
async def test_list_offers_empty(list_offers_usecase, offer_repository):
    offer_repository.list_offers = async_return([])
    
    output_dto = await list_offers_usecase.execute()
    
    assert len(output_dto.offers) == 0
    offer_repository.list_offers.await_count == 1