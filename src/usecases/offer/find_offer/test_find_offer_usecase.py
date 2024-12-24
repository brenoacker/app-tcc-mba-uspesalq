import random
from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from usecases.offer.find_offer.find_offer_dto import (FindOfferInputDto,
                                                      FindOfferOutputDto)
from usecases.offer.find_offer.find_offer_usecase import FindOfferUseCase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def find_offer_usecase(offer_repository):
    return FindOfferUseCase(offer_repository)

def test_find_offer_success(find_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.find_offer.return_value = offer
    
    input_dto = FindOfferInputDto(id=offer_id)
    
    output_dto = find_offer_usecase.execute(input=input_dto)
    
    assert output_dto.id == offer_id
    assert output_dto.discount_type == OfferType.PERCENTAGE
    assert output_dto.discount_value == 20.0
    offer_repository.find_offer.assert_called_once_with(offer_id=offer_id)

def test_find_offer_not_found(find_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer_repository.find_offer.return_value = None
    
    input_dto = FindOfferInputDto(id=offer_id)
    
    with pytest.raises(ValueError) as excinfo:
        _ = find_offer_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Offer with id '{offer_id}' not found"
    offer_repository.find_offer.assert_called_once_with(offer_id=offer_id)