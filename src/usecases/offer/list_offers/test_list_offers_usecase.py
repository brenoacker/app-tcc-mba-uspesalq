import random
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from usecases.offer.list_offers.list_offers_usecase import ListOffersUseCase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def list_offers_usecase(offer_repository):
    return ListOffersUseCase(offer_repository)

def test_list_offers_success(list_offers_usecase, offer_repository):
    offer_id = random.randint(1,100)
    offer = Offer(id=offer_id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10), discount_type=OfferType.PERCENTAGE, discount_value=20.0)
    offer_repository.list_offers.return_value = [offer]
    
    output_dto = list_offers_usecase.execute()
    
    assert len(output_dto.offers) == 1
    assert output_dto.offers[0].id == offer_id
    assert output_dto.offers[0].discount_type == OfferType.PERCENTAGE
    assert output_dto.offers[0].discount_value == 20.0
    offer_repository.list_offers.assert_called_once()

def test_list_offers_empty(list_offers_usecase, offer_repository):
    offer_repository.list_offers.return_value = []
    
    output_dto = list_offers_usecase.execute()
    
    assert len(output_dto.offers) == 0
    offer_repository.list_offers.assert_called_once()