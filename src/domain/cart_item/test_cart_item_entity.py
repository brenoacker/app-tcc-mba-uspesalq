from uuid import UUID, uuid4

import pytest

from domain.cart_item.cart_item_entity import CartItem


def test_cart_item_creation():
    cart_item_id = uuid4()
    cart_id = uuid4()
    product_id = 1
    quantity = 10

    cart_item = CartItem(id=cart_item_id, cart_id=cart_id, product_id=product_id, quantity=quantity)

    assert cart_item.id == cart_item_id
    assert cart_item.cart_id == cart_id
    assert cart_item.product_id == product_id
    assert cart_item.quantity == quantity

def test_cart_item_invalid_id():
    cart_id = uuid4()
    product_id = 1
    quantity = 10

    with pytest.raises(Exception) as excinfo:
        CartItem(id="invalid_uuid", cart_id=cart_id, product_id=product_id, quantity=quantity)
    assert str(excinfo.value) == "id must be an UUID"

def test_cart_item_invalid_cart_id():
    cart_item_id = uuid4()
    product_id = 1
    quantity = 10

    with pytest.raises(Exception) as excinfo:
        CartItem(id=cart_item_id, cart_id="invalid_uuid", product_id=product_id, quantity=quantity)
    assert str(excinfo.value) == "cart_id must be an UUID"

def test_cart_item_invalid_product_id():
    cart_item_id = uuid4()
    cart_id = uuid4()
    quantity = 10

    with pytest.raises(Exception) as excinfo:
        CartItem(id=cart_item_id, cart_id=cart_id, product_id="invalid_product_id", quantity=quantity)
    assert str(excinfo.value) == "product_id must be an integer"

def test_cart_item_invalid_quantity():
    cart_item_id = uuid4()
    cart_id = uuid4()
    product_id = 1

    with pytest.raises(Exception) as excinfo:
        CartItem(id=cart_item_id, cart_id=cart_id, product_id=product_id, quantity=-10)
    assert str(excinfo.value) == "quantity must be a positive integer"

    with pytest.raises(Exception) as excinfo:
        CartItem(id=cart_item_id, cart_id=cart_id, product_id=product_id, quantity="invalid_quantity")
    assert str(excinfo.value) == "quantity must be a positive integer"

def test_item_quantity():
    cart_item_id = uuid4()
    cart_id = uuid4()
    product_id = 1
    quantity = 10

    cart_item = CartItem(id=cart_item_id, cart_id=cart_id, product_id=product_id, quantity=quantity)
    assert cart_item.item_quantity() == quantity