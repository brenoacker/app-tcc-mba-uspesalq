from uuid import uuid4

import pytest

from domain.order_item.order_item_entity import OrderItem


def test_order_item_creation():
    order_item_id = uuid4()
    order_id = uuid4()
    product_id = uuid4()
    quantity = 2
    price = 50.0

    order_item = OrderItem(id=order_item_id, order_id=order_id, product_id=product_id, quantity=quantity, price=price)

    assert order_item.id == order_item_id
    assert order_item.order_id == order_id
    assert order_item.product_id == product_id
    assert order_item.quantity == quantity
    assert order_item.price == price

def test_order_item_invalid_id():
    order_id = uuid4()
    product_id = uuid4()
    quantity = 2
    price = 50.0

    with pytest.raises(Exception) as excinfo:
        OrderItem(id="invalid_uuid", order_id=order_id, product_id=product_id, quantity=quantity, price=price)
    assert str(excinfo.value) == "id must be an UUID"

def test_order_item_invalid_order_id():
    order_item_id = uuid4()
    product_id = uuid4()
    quantity = 2
    price = 50.0

    with pytest.raises(Exception) as excinfo:
        OrderItem(id=order_item_id, order_id="invalid_uuid", product_id=product_id, quantity=quantity, price=price)
    assert str(excinfo.value) == "order_id must be an UUID"

def test_order_item_invalid_product_id():
    order_item_id = uuid4()
    order_id = uuid4()
    quantity = 2
    price = 50.0

    with pytest.raises(Exception) as excinfo:
        OrderItem(id=order_item_id, order_id=order_id, product_id="invalid_uuid", quantity=quantity, price=price)
    assert str(excinfo.value) == "product_id must be an UUID"

def test_order_item_invalid_quantity():
    order_item_id = uuid4()
    order_id = uuid4()
    product_id = uuid4()
    price = 50.0

    with pytest.raises(Exception) as excinfo:
        OrderItem(id=order_item_id, order_id=order_id, product_id=product_id, quantity=-2, price=price)
    assert str(excinfo.value) == "quantity must be a positive integer"

    with pytest.raises(Exception) as excinfo:
        OrderItem(id=order_item_id, order_id=order_id, product_id=product_id, quantity="invalid_quantity", price=price)
    assert str(excinfo.value) == "quantity must be a positive integer"

def test_order_item_invalid_price():
    order_item_id = uuid4()
    order_id = uuid4()
    product_id = uuid4()
    quantity = 2

    with pytest.raises(Exception) as excinfo:
        OrderItem(id=order_item_id, order_id=order_id, product_id=product_id, quantity=quantity, price=-50.0)
    assert str(excinfo.value) == "price must be a non-negative number"

    with pytest.raises(Exception) as excinfo:
        OrderItem(id=order_item_id, order_id=order_id, product_id=product_id, quantity=quantity, price="invalid_price")
    assert str(excinfo.value) == "price must be a non-negative number"