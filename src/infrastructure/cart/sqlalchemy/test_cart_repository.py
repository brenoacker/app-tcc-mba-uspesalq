from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from domain.cart.cart_entity import Cart
from infrastructure.cart.sqlalchemy.cart_model import CartModel
from infrastructure.cart.sqlalchemy.cart_repository import CartRepository


@pytest.fixture
def session():
    return MagicMock()

@pytest.fixture
def cart_repository(session):
    return CartRepository(session)

def test_find_cart(cart_repository, session):
    cart_id = uuid4()
    user_id = uuid4()
    cart_model = CartModel(
        id=cart_id,
        user_id=user_id,
        total_price=100.0
    )
    session.query().filter().first.return_value = cart_model

    found_cart = cart_repository.find_cart(cart_id, user_id)

    assert found_cart.id == cart_id
    assert found_cart.user_id == user_id
    assert found_cart.total_price == 100.0

def test_find_cart_not_found(cart_repository, session):
    cart_id = uuid4()
    user_id = uuid4()
    session.query().filter().first.return_value = None

    found_cart = cart_repository.find_cart(cart_id, user_id)

    assert found_cart is None

def test_add_cart(cart_repository, session):
    cart_id = uuid4()
    user_id = uuid4()
    cart = Cart(
        id=cart_id,
        user_id=user_id,
        total_price=100.0
    )

    cart_repository.add_cart(cart)

    session.add.assert_called_once()
    session.commit.assert_called_once()

def test_update_cart(cart_repository, session):
    cart_id = uuid4()
    user_id = uuid4()
    cart = Cart(
        id=cart_id,
        user_id=user_id,
        total_price=150.0
    )
    cart_model = CartModel(
        id=cart_id,
        user_id=user_id,
        total_price=100.0
    )
    session.query().filter().first.return_value = cart_model

    updated_cart = cart_repository.update_cart(cart)

    session.query().filter().update.assert_called_once()
    session.commit.assert_called_once()
    assert updated_cart.id == cart_id
    assert updated_cart.user_id == user_id
    assert updated_cart.total_price == 100.0

def test_remove_cart(cart_repository, session):
    cart_id = uuid4()

    cart_repository.remove_cart(cart_id)

    session.query().filter().delete.assert_called_once()
    session.commit.assert_called_once()

def test_list_carts(cart_repository, session):
    user_id = uuid4()
    cart_model_1 = CartModel(
        id=uuid4(),
        user_id=user_id,
        total_price=100.0
    )
    cart_model_2 = CartModel(
        id=uuid4(),
        user_id=user_id,
        total_price=200.0
    )
    session.query().filter().all.return_value = [cart_model_1, cart_model_2]

    carts = cart_repository.list_carts(user_id)

    assert len(carts) == 2
    assert carts[0].id == cart_model_1.id
    assert carts[1].id == cart_model_2.id

def test_list_carts_not_found(cart_repository, session):
    user_id = uuid4()
    session.query().filter().all.return_value = []

    carts = cart_repository.list_carts(user_id)

    assert carts is None

def test_delete_all_carts(cart_repository, session):
    cart_repository.delete_all_carts()

    session.query().delete.assert_called_once()
    session.commit.assert_called_once()