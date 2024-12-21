import random
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType


def test_offer_creation():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    offer = Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)

    assert offer.id == offer_id
    assert offer.start_date == start_date
    assert offer.end_date == end_date
    assert offer.discount_type == discount_type
    assert offer.discount_value == discount_value

def test_offer_invalid_id():
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id="invalid_uuid", start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "id must be an integer"

def test_offer_with_negative_id():
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=-1, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "id must be greater than 0"

def test_offer_invalid_discount_type():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type="invalid_type", discount_value=discount_value)
    assert str(excinfo.value) == "discount_type must be an instance of OfferType"

def test_offer_invalid_discount_value():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=-10.0)
    assert str(excinfo.value) == "discount_value must be a positive number"

def test_offer_invalid_dates():
    offer_id = random.randint(1, 100)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, start_date=datetime.now() + timedelta(days=10), end_date=datetime.now() + timedelta(days=1), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "start_date must be before end_date"

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, start_date=datetime.now() - timedelta(days=10), end_date=datetime.now() - timedelta(days=1), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "end_date must be in the future"

def test_offer_is_active():
    offer_id = random.randint(1, 100)

    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    offer = Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert offer.is_active() is True

    offer = Offer(id=offer_id, start_date=datetime.now() + timedelta(days=1), end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert offer.is_active() is False

def test_offer_apply_discount():
    offer_id = random.randint(1, 100)

    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)

    offer = Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=OfferType.PERCENTAGE, discount_value=10.0)
    assert offer.apply_discount(100.0) == 90.0

    offer = Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=OfferType.AMOUNT, discount_value=10.0)
    assert offer.apply_discount(100.0) == 90.0
    assert offer.apply_discount(5.0) == 0.0

def test_offer_invalid_start_date():
    offer_id = random.randint(1, 100)

    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, start_date="invalid_date", end_date=datetime.now() + timedelta(days=10), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "start_date must be a datetime object"

def test_offer_invalid_end_date():
    offer_id = random.randint(1, 100)

    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, start_date=datetime.now() + timedelta(days=1), end_date="invalid_date", discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "end_date must be a datetime object"

def test_offer_start_date_after_end_date():
    offer_id = random.randint(1, 100)

    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, start_date=datetime.now() + timedelta(days=10), end_date=datetime.now() + timedelta(days=1), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "start_date must be before end_date"

def test_offer_end_date_in_past():
    offer_id = random.randint(1, 100)

    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, start_date=datetime.now() - timedelta(days=10), end_date=datetime.now() - timedelta(days=1), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "end_date must be in the future"
