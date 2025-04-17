import random
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from usecases.offer.add_offer.add_offer_dto import (AddOfferInputDto)
from usecases.offer.add_offer.add_offer_usecase import AddOfferUseCase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def add_offer_usecase(offer_repository):
    return AddOfferUseCase(offer_repository)

def test_add_offer_success(add_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer_repository.find_offer.return_value = None
    
    input_dto = AddOfferInputDto(id=offer_id, expiration_days=10, discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    
    added_offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.add_offer.return_value = added_offer
    
    output_dto = add_offer_usecase.execute(input=input_dto)
    
    assert output_dto.id == offer_id
    assert output_dto.discount_type == OfferType.PERCENTAGE
    assert output_dto.discount_value == 20.0
    assert output_dto.start_date <= datetime.now()
    assert output_dto.end_date >= datetime.now() + timedelta(days=9)
    offer_repository.find_offer.assert_called_once_with(offer_id=offer_id)
    offer_repository.add_offer.assert_called_once()

def test_add_offer_already_exists(add_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    existing_offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.find_offer.return_value = existing_offer
    
    input_dto = AddOfferInputDto(id=offer_id, expiration_days=10, discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    
    with pytest.raises(ValueError) as excinfo:
        add_offer_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Offer with id {offer_id} already exists"
    offer_repository.find_offer.assert_called_once_with(offer_id=offer_id)
    offer_repository.add_offer.assert_not_called()

def test_add_offer_invalid_expiration_days(add_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer_repository.find_offer.return_value = None
    
    input_dto = AddOfferInputDto(id=offer_id, expiration_days=0, discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    
    with pytest.raises(ValueError) as excinfo:
        add_offer_usecase.execute(input=input_dto)
    assert str(excinfo.value) == "Expiration days must be greater than 0"
    offer_repository.find_offer.assert_called_once_with(offer_id=offer_id)
    offer_repository.add_offer.assert_not_called()