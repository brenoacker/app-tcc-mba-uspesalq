import random
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from usecases.offer.add_offer.add_offer_dto import (AddOfferInputDto,
                                                    AddOfferOutputDto)
from usecases.offer.add_offer.add_offer_usecase import AddOfferUseCase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def add_offer_usecase(offer_repository):
    return AddOfferUseCase(offer_repository)

@pytest.mark.asyncio
async def test_add_offer_success(add_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer_repository.find_offer = async_return(None)
    
    input_dto = AddOfferInputDto(id=offer_id, expiration_days=10, discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    
    added_offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.add_offer = async_return(added_offer)
    
    output_dto = await add_offer_usecase.execute(input=input_dto)
    
    assert output_dto.id == offer_id
    assert output_dto.discount_type == OfferType.PERCENTAGE
    assert output_dto.discount_value == 20.0
    assert output_dto.start_date <= datetime.now()
    assert output_dto.end_date >= datetime.now() + timedelta(days=9)
    offer_repository.find_offer.assert_awaited_once_with()
    offer_repository.add_offer.await_count == 1

@pytest.mark.asyncio
async def test_add_offer_already_exists(add_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    existing_offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.find_offer = async_return(existing_offer)
    
    input_dto = AddOfferInputDto(id=offer_id, expiration_days=10, discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    
    with pytest.raises(ValueError) as excinfo:
        run_async(add_offer_usecase.execute(input=input_dto))
    assert str(excinfo.value) == f"Offer with id {offer_id} already exists"
    offer_repository.find_offer.assert_awaited_once_with()
    offer_repository.add_offer.called == False

@pytest.mark.asyncio
async def test_add_offer_invalid_expiration_days(add_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer_repository.find_offer = async_return(None)
    
    input_dto = AddOfferInputDto(id=offer_id, expiration_days=0, discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    
    with pytest.raises(ValueError) as excinfo:
        run_async(add_offer_usecase.execute(input=input_dto))
    assert str(excinfo.value) == "Expiration days must be greater than 0"
    offer_repository.find_offer.assert_awaited_once_with()
    offer_repository.add_offer.called == False