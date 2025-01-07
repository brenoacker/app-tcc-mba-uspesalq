from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

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

def test_add_offer(offer_repository, session):
    offer = Offer(
        id=1,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
        discount_type=OfferType.PERCENTAGE,
        discount_value=10.0
    )

    added_offer = offer_repository.add_offer(offer)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    assert added_offer.id == offer.id
    assert added_offer.start_date == offer.start_date
    assert added_offer.end_date == offer.end_date
    assert added_offer.discount_type == offer.discount_type
    assert added_offer.discount_value == offer.discount_value

def test_find_offer(offer_repository, session):
    offer_id = 1
    offer_model = OfferModel(
        id=offer_id,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
        discount_type=OfferType.PERCENTAGE,
        discount_value=10.0
    )
    session.query().filter().first.return_value = offer_model

    found_offer = offer_repository.find_offer(offer_id)

    assert found_offer.id == offer_id
    assert found_offer.start_date == offer_model.start_date
    assert found_offer.end_date == offer_model.end_date
    assert found_offer.discount_type == offer_model.discount_type
    assert found_offer.discount_value == offer_model.discount_value

def test_find_offer_not_found(offer_repository, session):
    offer_id = 1
    session.query().filter().first.return_value = None

    found_offer = offer_repository.find_offer(offer_id)

    assert found_offer is None

def test_list_offers(offer_repository, session):
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
    session.query().all.return_value = [offer_model_1, offer_model_2]

    offers = offer_repository.list_offers()

    assert len(offers) == 2
    assert offers[0].id == offer_model_1.id
    assert offers[1].id == offer_model_2.id

def test_list_offers_empty(offer_repository, session):
    session.query().all.return_value = []

    offers = offer_repository.list_offers()

    assert offers is None

def test_remove_offer(offer_repository, session):
    offer_id = 1

    offer_repository.remove_offer(offer_id)

    session.query().filter().delete.assert_called_once()
    session.commit.assert_called_once()

def test_remove_all_offers_success(offer_repository, session):
    # Act
    result = offer_repository.remove_all_offers()

    # Assert
    session.query(OfferModel).delete.assert_called_once()
    session.commit.assert_called_once()
    assert result is None