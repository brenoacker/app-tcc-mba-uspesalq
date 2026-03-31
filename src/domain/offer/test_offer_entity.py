import random
from datetime import datetime, timedelta
from decimal import Decimal # Added

import pytest

# from domain.__seedwork.test_utils import run_async # Not used
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType


@pytest.mark.asyncio
async def test_offer_creation():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = Decimal('10.0') # Changed

    offer = Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)

    assert offer.id == offer_id
    assert offer.start_date == start_date
    assert offer.end_date == end_date
    assert offer.discount_type == discount_type
    assert offer.discount_value == discount_value # Compares Decimals

@pytest.mark.asyncio
async def test_offer_invalid_id_type(): # Renamed
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = Decimal('10.0') # Changed

    with pytest.raises(TypeError) as excinfo: # Changed
        Offer(id="invalid_uuid_or_string", start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "id must be an integer"

@pytest.mark.asyncio
async def test_offer_with_negative_id_value(): # Renamed
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = Decimal('10.0') # Changed

    with pytest.raises(ValueError) as excinfo: # Changed
        Offer(id=-1, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "id must be greater than 0"

@pytest.mark.asyncio
async def test_offer_invalid_discount_type():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_value = Decimal('10.0') # Changed

    with pytest.raises(TypeError) as excinfo: # Changed
        Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type="invalid_type", discount_value=discount_value)
    assert str(excinfo.value) == "discount_type must be an instance of OfferType"

@pytest.mark.asyncio
async def test_offer_negative_discount_value(): # Renamed
    offer_id = random.randint(1, 100)
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE

    with pytest.raises(ValueError) as excinfo: # Changed
        Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value=Decimal('-10.0')) # Changed
    assert str(excinfo.value) == "discount_value must be a positive number" # Message from Offer.validate

@pytest.mark.asyncio
async def test_offer_constructor_invalid_discount_value_type():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE

    with pytest.raises(TypeError) as excinfo:
        Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=discount_type, discount_value="not_a_decimal")
    assert str(excinfo.value) == "discount_value must be float or Decimal" # Message from Offer.__init__

@pytest.mark.asyncio
async def test_offer_invalid_dates_order(): # Renamed
    offer_id = random.randint(1, 100)
    discount_type = OfferType.PERCENTAGE
    discount_value = Decimal('10.0') # Changed

    with pytest.raises(ValueError) as excinfo: # Changed
        Offer(id=offer_id, start_date=datetime.now() + timedelta(days=10), end_date=datetime.now() + timedelta(days=1), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "start_date must be before end_date"

@pytest.mark.asyncio
async def test_offer_end_date_in_past_validation(): # Renamed
    offer_id = random.randint(1, 100)
    discount_type = OfferType.PERCENTAGE
    discount_value = Decimal('10.0') # Changed
    with pytest.raises(ValueError) as excinfo: # Changed
        Offer(id=offer_id, start_date=datetime.now() - timedelta(days=10), end_date=datetime.now() - timedelta(days=1), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "end_date must be in the future" # Message from Offer.validate

@pytest.mark.asyncio
async def test_offer_is_active():
    offer_id = random.randint(1, 100)
    start_date_active = datetime.now() - timedelta(days=1)
    end_date_active = datetime.now() + timedelta(days=10)
    discount_type = OfferType.PERCENTAGE
    discount_value = Decimal('10.0') # Changed

    offer_active = Offer(id=offer_id, start_date=start_date_active, end_date=end_date_active, discount_type=discount_type, discount_value=discount_value)
    assert offer_active.is_active() is True

    start_date_inactive = datetime.now() + timedelta(days=1)
    end_date_inactive = datetime.now() + timedelta(days=5)
    offer_inactive = Offer(id=offer_id + 1, start_date=start_date_inactive, end_date=end_date_inactive, discount_type=discount_type, discount_value=discount_value)
    assert offer_inactive.is_active() is False

@pytest.mark.asyncio
async def test_offer_apply_discount():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() - timedelta(days=1) # Ensure active for test
    end_date = datetime.now() + timedelta(days=10)

    # Percentage discount
    offer_percentage = Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=OfferType.PERCENTAGE, discount_value=Decimal('10.0')) # 10%
    price1 = Decimal('100.00')
    expected1 = Decimal('90.00')
    assert offer_percentage.apply_discount(price1) == expected1

    price2 = Decimal('199.99')
    # 199.99 * 10/100 = 19.999.  199.99 - 19.999 = 179.991. Rounded to 179.99
    expected2 = Decimal('179.99') 
    assert offer_percentage.apply_discount(price2) == expected2
    
    # Amount discount
    offer_amount = Offer(id=offer_id + 1, start_date=start_date, end_date=end_date, discount_type=OfferType.AMOUNT, discount_value=Decimal('15.50'))
    price3 = Decimal('100.00')
    expected3 = Decimal('84.50')
    assert offer_amount.apply_discount(price3) == expected3

    price4 = Decimal('5.25') # Price less than discount
    expected4 = Decimal('0.00')
    assert offer_amount.apply_discount(price4) == expected4
    
    # Test apply_discount with float input (should be converted by the method)
    price_float = 50.0
    expected_float_percentage = Decimal('45.00') # 50.0 * 10% = 5.0 discount
    assert offer_percentage.apply_discount(price_float) == expected_float_percentage
    
    expected_float_amount = Decimal('34.50') # 50.0 - 15.50
    assert offer_amount.apply_discount(price_float) == expected_float_amount


@pytest.mark.asyncio
async def test_offer_invalid_start_date_type(): # Renamed
    offer_id = random.randint(1, 100)
    discount_type = OfferType.PERCENTAGE
    discount_value = Decimal('10.0') # Changed

    with pytest.raises(TypeError) as excinfo: # Changed
        Offer(id=offer_id, start_date="invalid_date_string", end_date=datetime.now() + timedelta(days=10), discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "start_date must be a datetime object"

@pytest.mark.asyncio
async def test_offer_invalid_end_date_type(): # Renamed
    offer_id = random.randint(1, 100)
    discount_type = OfferType.PERCENTAGE
    discount_value = Decimal('10.0') # Changed

    with pytest.raises(TypeError) as excinfo: # Changed
        Offer(id=offer_id, start_date=datetime.now() + timedelta(days=1), end_date="invalid_date_string", discount_type=discount_type, discount_value=discount_value)
    assert str(excinfo.value) == "end_date must be a datetime object"

# test_offer_start_date_after_end_date and test_offer_end_date_in_past are effectively covered by
# test_offer_invalid_dates_order and test_offer_end_date_in_past_validation respectively.
# Can remove them if they are exact duplicates or keep if subtle differences intended.
# For now, I'll assume they are covered and removed the redundant ones from my mental model of this overwrite.
# The provided file had them, so I've updated them above. The names were already specific.

@pytest.mark.asyncio
async def test_offer_apply_discount_invalid_percentage_value():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    price = Decimal('100.00')

    # Percentage > 100
    with pytest.raises(ValueError) as excinfo:
        offer_invalid_percentage = Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=OfferType.PERCENTAGE, discount_value=Decimal('101.0'))
        offer_invalid_percentage.apply_discount(price)
    assert str(excinfo.value) == "Percentage discount_value must be between 0 and 100."

    # Percentage < 0 (already covered by general discount_value < 0 validation in __init__)
    # but apply_discount also has a specific check for percentage range.
    # If __init__ catches negative discount_value, this specific check in apply_discount for <0 might be redundant
    # or only for >100. The current Offer.apply_discount checks for <0 and >100.
    # Let's assume __init__ already validated that discount_value is not < 0.
    # The test for negative discount_value in constructor is test_offer_negative_discount_value.
    # So this test should focus on > 100 or if apply_discount has different logic.
    # The current Offer.apply_discount has `if self.discount_value < Decimal('0') or self.discount_value > Decimal('100'):`
    # This is fine.
    
    # Test with discount_value that becomes negative due to __init__ not catching it (if that were the case)
    # However, __init__ *does* validate discount_value >= 0.
    # So, this test will primarily test the > 100 case for percentage in apply_discount.
    # The test_offer_negative_discount_value already covers the < 0 case at construction.

@pytest.mark.asyncio
async def test_offer_apply_discount_type_error_on_price():
    offer_id = random.randint(1, 100)
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=10)
    offer = Offer(id=offer_id, start_date=start_date, end_date=end_date, discount_type=OfferType.PERCENTAGE, discount_value=Decimal('10.0'))
    
    with pytest.raises(TypeError) as excinfo:
        offer.apply_discount("not_a_decimal_or_float")
    assert str(excinfo.value) == "price must be a Decimal or float" # As per Offer.apply_discount
