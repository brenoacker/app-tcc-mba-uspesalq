import random
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from usecases.offer.remove_offer.remove_offer_dto import RemoveOfferInputDto
from usecases.offer.remove_offer.remove_offer_usecase import RemoveOfferUseCase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def remove_offer_usecase(offer_repository):
    return RemoveOfferUseCase(offer_repository)

def test_remove_offer_success(remove_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.find_offer.return_value = offer
    
    input_dto = RemoveOfferInputDto(id=offer_id)
    
    remove_offer_usecase.execute(input=input_dto)
    
    offer_repository.find_offer.assert_called_once_with(offer_id)
    offer_repository.remove_offer.assert_called_once_with(offer_id)

def test_remove_offer_not_found(remove_offer_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer_repository.find_offer.return_value = None
    
    input_dto = RemoveOfferInputDto(id=offer_id)
    
    with pytest.raises(ValueError) as excinfo:
        remove_offer_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Offer with id {offer_id} not found"
    offer_repository.find_offer.assert_called_once_with(offer_id)
    offer_repository.remove_offer.assert_not_called()