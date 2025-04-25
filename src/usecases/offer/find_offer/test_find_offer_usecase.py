import random
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from usecases.offer.find_offer.find_offer_dto import FindOfferInputDto
from usecases.offer.find_offer.find_offer_usecase import FindOfferUseCase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def find_offer_usecase(offer_repository):
    return FindOfferUseCase(offer_repository)

@pytest.mark.asyncio
async def test_find_offer_success(find_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.find_offer = async_return(offer)
    
    input_dto = FindOfferInputDto(id=offer_id)
    
    # Substituindo run_async por await
    output_dto = await find_offer_usecase.execute(input=input_dto)
    
    assert output_dto.id == offer_id
    assert output_dto.discount_type == OfferType.PERCENTAGE
    assert output_dto.discount_value == 20.0
    offer_repository.find_offer.assert_awaited_once_with(offer_id=offer_id)

@pytest.mark.asyncio
async def test_find_offer_not_found(find_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer_repository.find_offer = async_return(None)
    
    input_dto = FindOfferInputDto(id=offer_id)
    
    with pytest.raises(ValueError) as excinfo:
        # Substituindo run_async por await
        await find_offer_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Offer with id '{offer_id}' not found"
    # Corrigindo para incluir o parâmetro nomeado
    offer_repository.find_offer.assert_awaited_once_with(offer_id=offer_id)