from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType


def test_offer_creation():
    offer_id = uuid4()
    product_id = uuid4()
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    offer = Offer(id=offer_id, product_id=product_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)

    assert offer.id == offer_id
    assert offer.product_id == product_id
    assert offer.start_date == start_date
    assert offer.end_date == end_date
    assert offer.discount_type == discount_type
    assert offer.discount_value == discount_value

def test_offer_invalid_id():
    product_id = uuid4()
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id="invalid_uuid", product_id=product_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "id must be an UUID"

def test_offer_invalid_product_id():
    offer_id = uuid4()
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, product_id="invalid_uuid", start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "product_id must be an UUID"

def test_offer_invalid_discount_type():
    offer_id = uuid4()
    product_id = uuid4()
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, product_id=product_id, start_date=start_date, end_date=end_date, discount_type="invalid_type", discount_value=discount_value)
    assert str(excinfo.value) == "discount_type must be an instance of OfferType"

def test_offer_invalid_discount_value():
    offer_id = uuid4()
    product_id = uuid4()
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, product_id=product_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=-10.0)
    assert str(excinfo.value) == "discount_value must be a positive number"

def test_offer_invalid_dates():
    offer_id = uuid4()
    product_id = uuid4()
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, product_id=product_id, start_date=datetime.now() + timedelta(days=10), end_date=datetime.now() + timedelta(days=1), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "start_date must be before end_date"

    with pytest.raises(Exception) as excinfo:
        Offer(id=offer_id, product_id=product_id, start_date=datetime.now() - timedelta(days=10), end_date=datetime.now() - timedelta(days=1), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "end_date must be in the future"

def test_offer_is_active():
    offer_id = uuid4()
    product_id = uuid4()
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = 10.0

    offer = Offer(id=offer_id, product_id=product_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert offer.is_active() is True

    offer = Offer(id=offer_id, product_id=product_id, start_date=datetime.now() + timedelta(days=1), end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert offer.is_active() is False

def test_offer_apply_discount():
    offer_id = uuid4()
    product_id = uuid4()
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)

    offer = Offer(id=offer_id, product_id=product_id, start_date=start_date, end_date=end_date, discount_type=OfferType.PERCENTAGE, discount_value=10.0)
    assert offer.apply_discount(100.0) == 90.0

    offer = Offer(id=offer_id, product_id=product_id, start_date=start_date, end_date=end_date, discount_type=OfferType.AMOUNT, discount_value=10.0)
    assert offer.apply_discount(100.0) == 90.0
    assert offer.apply_discount(5.0) == 0.0