import random
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from domain.order_item.order_item_entity import OrderItem


def test_order_creation():
    order_id = uuid4()
    user_id = uuid4()
    offer_id = random.randint(1, 100)
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100.0

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

def test_order_invalid_id():
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Order(id="invalid_uuid", user_id=user_id, cart_id=cart_id,  total_price=total_price, type=type, status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "id must be an UUID"

def test_order_invalid_user_id():
    order_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id="invalid_uuid", cart_id=cart_id,  total_price=total_price, type=type, status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "user_id must be an UUID"

def test_order_invalid_total_price():
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100.0

    order = Order(id=order_id, user_id=user_id, total_price=total_price, type=type, cart_id=cart_id, status=status, created_at=created_at, updated_at=updated_at)
    order.total_price = -100.0

    with pytest.raises(Exception) as excinfo:
        order.validate()
    assert str(excinfo.value) == "total_price must be a non-negative number"

def test_order_invalid_status():
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, total_price=total_price, type=type, cart_id=cart_id, status="invalid_status", created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "status must be an instance of OrderStatus"

def test_order_invalid_dates():
    order_id = uuid4()
    user_id = uuid4()
    cart_id= uuid4() 
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, cart_id=cart_id, type=type, total_price=total_price, status=status, created_at="invalid_date", updated_at=datetime.now())
    assert str(excinfo.value) == "created_at must be a datetime object"

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, cart_id=cart_id, type=type, status=status, total_price=total_price, created_at=datetime.now(), updated_at="invalid_date")
    assert str(excinfo.value) == "updated_at must be a datetime object"

def test_order_invalid_offer_id():
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, cart_id=cart_id,  type=type, total_price=total_price, status=status, created_at=created_at, updated_at=updated_at, offer_id="invalid_uuid")
    assert str(excinfo.value) == "offer_id must be an int or None"

def test_order_with_invalid_cart_id():
    order_id = uuid4()
    user_id = uuid4()
    cart_id = random.randint(1,100)
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, cart_id=cart_id,  type=type, total_price=total_price, status=status, created_at=created_at, updated_at=updated_at, offer_id="invalid_uuid")
    assert str(excinfo.value) == "cart_id must be an UUID"

def test_order_with_invalid_total_price():
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    type = OrderType.DELIVERY
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, cart_id=cart_id,  type=type, total_price=total_price, status=status, created_at=created_at, updated_at=updated_at, offer_id="invalid_uuid")
    assert str(excinfo.value) == "total_price must be float"

def test_order_with_invalid_type():
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, cart_id=cart_id,  total_price=total_price, type="invalid_type", status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "type must be an instance of OrderType"