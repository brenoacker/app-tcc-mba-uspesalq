from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order_item.order_item_entity import OrderItem


def test_order_creation():
    order_id = uuid4()
    user_id = uuid4()
    offer_id = uuid4()
    items = [OrderItem(id=uuid4(), order_id=order_id, product_id=uuid4(), quantity=2, price=50.0)]
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    order = Order(id=order_id, user_id=user_id, items=items, status=status, created_at=created_at, updated_at=updated_at, offer_id=offer_id)

    assert order.id == order_id
    assert order.user_id == user_id
    assert order.offer_id == offer_id
    assert order.items == items
    assert order.total_amount == 100.0
    assert order.status == status
    assert order.created_at == created_at
    assert order.updated_at == updated_at

def test_order_invalid_id():
    user_id = uuid4()
    items = [OrderItem(id=uuid4(), order_id=uuid4(), product_id=uuid4(), quantity=2, price=50.0)]
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Order(id="invalid_uuid", user_id=user_id, items=items, status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "id must be an UUID"

def test_order_invalid_user_id():
    order_id = uuid4()
    items = [OrderItem(id=uuid4(), order_id=order_id, product_id=uuid4(), quantity=2, price=50.0)]
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id="invalid_uuid", items=items, status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "user_id must be an UUID"

def test_order_invalid_total_amount():
    order_id = uuid4()
    user_id = uuid4()
    items = [OrderItem(id=uuid4(), order_id=order_id, product_id=uuid4(), quantity=2, price=50.0)]
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    order = Order(id=order_id, user_id=user_id, items=items, status=status, created_at=created_at, updated_at=updated_at)
    order.total_amount = -100.0

    with pytest.raises(Exception) as excinfo:
        order.validate()
    assert str(excinfo.value) == "total_amount must be a non-negative number"

def test_order_invalid_status():
    order_id = uuid4()
    user_id = uuid4()
    items = [OrderItem(id=uuid4(), order_id=order_id, product_id=uuid4(), quantity=2, price=50.0)]
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, items=items, status="invalid_status", created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "status must be an instance of OrderStatus"

def test_order_invalid_dates():
    order_id = uuid4()
    user_id = uuid4()
    items = [OrderItem(id=uuid4(), order_id=order_id, product_id=uuid4(), quantity=2, price=50.0)]
    status = OrderStatus.PENDING

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, items=items, status=status, created_at="invalid_date", updated_at=datetime.now())
    assert str(excinfo.value) == "created_at must be a datetime object"

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, items=items, status=status, created_at=datetime.now(), updated_at="invalid_date")
    assert str(excinfo.value) == "updated_at must be a datetime object"

def test_order_invalid_offer_id():
    order_id = uuid4()
    user_id = uuid4()
    items = [OrderItem(id=uuid4(), order_id=order_id, product_id=uuid4(), quantity=2, price=50.0)]
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Order(id=order_id, user_id=user_id, items=items, status=status, created_at=created_at, updated_at=updated_at, offer_id="invalid_uuid")
    assert str(excinfo.value) == "offer_id must be an UUID or None"

def test_order_calculate_total_amount():
    order_id = uuid4()
    user_id = uuid4()
    items = [OrderItem(id=uuid4(), order_id=order_id, product_id=uuid4(), quantity=2, price=50.0)]
    status = OrderStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    order = Order(id=order_id, user_id=user_id, items=items, status=status, created_at=created_at, updated_at=updated_at)
    assert order.calculate_total_amount() == 100.0