from decimal import Decimal # Added
from uuid import uuid4

import pytest

# from domain.__seedwork.test_utils import run_async # Not used
from domain.cart.cart_entity import Cart


@pytest.mark.asyncio
async def test_cart_creation():
    cart_id = uuid4()
    user_id = uuid4()
    total_price = Decimal('100.00') # Changed

    cart = Cart(id=cart_id, user_id=user_id, total_price=total_price)

    assert cart.id == cart_id
    assert cart.user_id == user_id
    assert cart.total_price == total_price # Compares Decimals

@pytest.mark.asyncio
async def test_cart_invalid_id_type(): # Renamed
    user_id = uuid4()
    total_price = Decimal('100.00') # Changed

    with pytest.raises(TypeError) as excinfo: # Changed
        Cart(id="invalid_uuid_string", user_id=user_id, total_price=total_price)
    assert str(excinfo.value) == "id must be an UUID" # Message from Cart.validate()

@pytest.mark.asyncio
async def test_cart_invalid_user_id_type(): # Renamed
    cart_id = uuid4()
    total_price = Decimal('100.00') # Changed

    with pytest.raises(TypeError) as excinfo: # Changed
        Cart(id=cart_id, user_id="invalid_uuid_string", total_price=total_price)
    assert str(excinfo.value) == "user_id must be an UUID" # Message from Cart.validate()

@pytest.mark.asyncio
async def test_cart_constructor_invalid_total_price(): # Renamed
    cart_id = uuid4()
    user_id = uuid4()

    # Test negative total_price
    with pytest.raises(ValueError) as excinfo_negative: # Changed
        Cart(id=cart_id, user_id=user_id, total_price=Decimal('-10.00')) # Changed
    # Message from Cart.set_total_price()
    assert str(excinfo_negative.value) == "total_price must be a non-negative number" 

    # Test invalid type for total_price
    with pytest.raises(TypeError) as excinfo_type: # Changed
        Cart(id=cart_id, user_id=user_id, total_price="invalid_price_string")
    # Message from Cart.set_total_price()
    assert str(excinfo_type.value) == "total_price must be a number (float, Decimal, or int)"

@pytest.mark.asyncio
async def test_cart_set_total_price_direct():
    cart_id = uuid4()
    user_id = uuid4()
    cart = Cart(id=cart_id, user_id=user_id, total_price=Decimal('50.00'))

    # Valid update
    cart.total_price = cart.set_total_price(Decimal('123.45'))
    assert cart.total_price == Decimal('123.45')

    cart.total_price = cart.set_total_price(75.50) # float input
    assert cart.total_price == Decimal('75.50')

    cart.total_price = cart.set_total_price(200) # int input
    assert cart.total_price == Decimal('200.00')

    # Invalid update - negative
    with pytest.raises(ValueError) as excinfo_negative:
        cart.set_total_price(Decimal('-0.01'))
    assert str(excinfo_negative.value) == "total_price must be a non-negative number"

    # Invalid update - type
    with pytest.raises(TypeError) as excinfo_type:
        cart.set_total_price("not_a_number")
    assert str(excinfo_type.value) == "total_price must be a number (float, Decimal, or int)"

@pytest.mark.asyncio
async def test_cart_total_price_precision():
    cart_id = uuid4()
    user_id = uuid4()
    
    # Test precision from float
    cart1 = Cart(id=cart_id, user_id=user_id, total_price=123.456)
    assert cart1.total_price == Decimal('123.46') # Rounds up

    # Test precision from string Decimal
    cart2 = Cart(id=uuid4(), user_id=user_id, total_price=Decimal('78.987'))
    assert cart2.total_price == Decimal('78.99') # Rounds up

    cart3 = Cart(id=uuid4(), user_id=user_id, total_price=Decimal('10.123'))
    assert cart3.total_price == Decimal('10.12') # Rounds down
    
    cart4 = Cart(id=uuid4(), user_id=user_id, total_price=0)
    assert cart4.total_price == Decimal('0.00')
