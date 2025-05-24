import random
from datetime import datetime
from decimal import Decimal # Added
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import run_async
from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType


@pytest.mark.asyncio
async def test_order_creation():
    order_id = uuid4()
    user_id = uuid4()
    offer_id = random.randint(1, 100)
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = Decimal('100.00') # Changed to Decimal

    order = Order(id=order_id, user_id=user_id,  total_price=total_price, type=type, cart_id=cart_id, status=status, created_at=created_at, updated_at=updated_at, offer_id=offer_id)

    assert order.id == order_id
    assert order.user_id == user_id
    assert order.offer_id == offer_id
    assert order.cart_id == cart_id
    assert order.status == status
    assert order.created_at == created_at
    assert order.updated_at == updated_at
    assert order.total_price == total_price
    assert order.type == type

@pytest.mark.asyncio
async def test_order_invalid_id():
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = Decimal('100.00') # Changed to Decimal

    with pytest.raises(TypeError) as excinfo: # Changed to TypeError
        Order(id="invalid_uuid", user_id=user_id, cart_id=cart_id,  total_price=total_price, type=type, status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "id must be an UUID"

@pytest.mark.asyncio
async def test_order_invalid_user_id():
    order_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = Decimal('100.00') # Changed to Decimal

    with pytest.raises(TypeError) as excinfo: # Changed to TypeError
        Order(id=order_id, user_id="invalid_uuid", cart_id=cart_id,  total_price=total_price, type=type, status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "user_id must be an UUID"

@pytest.mark.asyncio
async def test_order_validate_negative_total_price(): # Renamed for clarity
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    # total_price = Decimal('100.00') # Initial valid price, not strictly needed for this test path

    # Test that __init__ (which calls validate) catches a negative price passed.
    with pytest.raises(ValueError) as excinfo: # Changed to ValueError
        Order(id=order_id, user_id=user_id, cart_id=cart_id,  type=type, total_price=Decimal('-100.00'), status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "total_price must be a non-negative number"

@pytest.mark.asyncio
async def test_order_invalid_status_type(): # Renamed for clarity
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = Decimal('100.00') # Changed to Decimal

    with pytest.raises(TypeError) as excinfo: # Changed to TypeError
        Order(id=order_id, user_id=user_id, total_price=total_price, type=type, cart_id=cart_id, status="invalid_status_string", created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "status must be an instance of OrderStatus"

@pytest.mark.asyncio
async def test_order_invalid_date_types(): # Renamed for clarity
    order_id = uuid4()
    user_id = uuid4()
    cart_id= uuid4() 
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    total_price = Decimal('100.00') # Changed to Decimal

    with pytest.raises(TypeError) as excinfo_created_at: # Changed to TypeError
        Order(id=order_id, user_id=user_id, cart_id=cart_id, type=type, total_price=total_price, status=status, created_at="invalid_date_string", updated_at=datetime.now())
    assert str(excinfo_created_at.value) == "created_at must be a datetime object"

    with pytest.raises(TypeError) as excinfo_updated_at: # Changed to TypeError
        Order(id=order_id, user_id=user_id, cart_id=cart_id, type=type, status=status, total_price=total_price, created_at=datetime.now(), updated_at="invalid_date_string")
    assert str(excinfo_updated_at.value) == "updated_at must be a datetime object"

@pytest.mark.asyncio
async def test_order_invalid_offer_id_type(): # Renamed for clarity
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = Decimal('100.00') # Changed to Decimal

    with pytest.raises(TypeError) as excinfo: # Changed to TypeError
        Order(id=order_id, user_id=user_id, cart_id=cart_id,  type=type, total_price=total_price, status=status, created_at=created_at, updated_at=updated_at, offer_id="invalid_offer_id_string")
    assert str(excinfo.value) == "offer_id must be an int or None"

@pytest.mark.asyncio
async def test_order_with_invalid_cart_id_type(): # Renamed for clarity
    order_id = uuid4()
    user_id = uuid4()
    # cart_id was random.randint(1,100) which is an int. Test should use a string.
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = Decimal('100.00') # Changed to Decimal

    with pytest.raises(TypeError) as excinfo: # Changed to TypeError
        Order(id=order_id, user_id=user_id, cart_id="invalid_cart_id_string",  type=type, total_price=total_price, status=status, created_at=created_at, updated_at=updated_at, offer_id=None)
    assert str(excinfo.value) == "cart_id must be an UUID"

@pytest.mark.asyncio
async def test_order_constructor_invalid_total_price_type(): # Renamed and logic corrected
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    
    # Test with an integer. Based on Order.set_total_price: 
    # `if not isinstance(total_price, (float, Decimal)): raise TypeError("total_price must be float or Decimal")`
    # An int should raise this TypeError because my Order.set_total_price expects float or Decimal only.
    total_price_int = 100 

    with pytest.raises(TypeError) as excinfo: 
        Order(id=order_id, user_id=user_id, cart_id=cart_id,  type=type, total_price=total_price_int, status=status, created_at=created_at, updated_at=updated_at, offer_id=None)
    assert str(excinfo.value) == "total_price must be float or Decimal" # Message from Order.set_total_price

@pytest.mark.asyncio
async def test_order_with_invalid_order_type_type(): # Renamed for clarity
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = Decimal('100.00') # Changed to Decimal

    with pytest.raises(TypeError) as excinfo: # Changed to TypeError
        Order(id=order_id, user_id=user_id, cart_id=cart_id,  total_price=total_price, type="invalid_type_string", status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "type must be an instance of OrderType"