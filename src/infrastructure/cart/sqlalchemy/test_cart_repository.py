from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.cart.cart_entity import Cart
from infrastructure.cart.sqlalchemy.cart_model import CartModel
from infrastructure.cart.sqlalchemy.cart_repository import CartRepository


@pytest.fixture
def session():
    return MagicMock()

@pytest.fixture
def cart_repository(session):
    return CartRepository(session)

@pytest.mark.asyncio
async def test_find_cart(cart_repository, session):
    cart_id = uuid4()
    user_id = uuid4()
    cart_model = CartModel(
        id=cart_id,
        user_id=user_id,
        total_price=100.0
    )
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = cart_model

    found_cart = await cart_repository.find_cart(cart_id, user_id)

    assert found_cart.id == cart_id
    assert found_cart.user_id == user_id
    assert found_cart.total_price == 100.0

@pytest.mark.asyncio
async def test_find_cart_not_found(cart_repository, session):
    cart_id = uuid4()
    user_id = uuid4()
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = None

    found_cart = await cart_repository.find_cart(cart_id, user_id)

    assert found_cart is None

@pytest.mark.asyncio
async def test_add_cart(cart_repository, session):
    cart_id = uuid4()
    user_id = uuid4()
    cart = Cart(
        id=cart_id,
        user_id=user_id,
        total_price=100.0
    )
    session.commit = async_return(None)

    await cart_repository.add_cart(cart)

    # Check that the session methods were called
    assert session.add.called
    assert session.commit.called

@pytest.mark.asyncio
async def test_update_cart(cart_repository, session):
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
    
    # First execute for update
    update_execute_result = MagicMock()
    
    # Second execute for select
    select_execute_result = MagicMock()
    select_execute_result.scalars.return_value.first.return_value = cart_model
    
    # Set up execute to return different results for each call
    session.execute = AsyncMock()
    session.execute.side_effect = [update_execute_result, select_execute_result]
    
    # Set up commit to be awaitable
    session.commit = AsyncMock()

    updated_cart = await cart_repository.update_cart(cart)

    # Verify method was called
    assert session.execute.call_count == 2
    assert session.commit.called
    
    # Verify the returned cart has the correct values
    assert updated_cart.id == cart_id
    assert updated_cart.user_id == user_id
    assert updated_cart.total_price == 100.0

@pytest.mark.asyncio
async def test_remove_cart(cart_repository, session):
    cart_id = uuid4()
    
    session.execute = async_return(MagicMock())
    session.commit = async_return(None)

    await cart_repository.remove_cart(cart_id)

    assert session.execute.called
    assert session.commit.called

@pytest.mark.asyncio
async def test_list_carts(cart_repository, session):
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
    
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.all.return_value = [cart_model_1, cart_model_2]

    carts = await cart_repository.list_carts(user_id)

    assert len(carts) == 2
    assert carts[0].id == cart_model_1.id
    assert carts[1].id == cart_model_2.id

@pytest.mark.asyncio
async def test_list_carts_not_found(cart_repository, session):
    user_id = uuid4()
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.all.return_value = []

    carts = await cart_repository.list_carts(user_id)

    assert carts is None

@pytest.mark.asyncio
async def test_delete_all_carts(cart_repository, session):
    session.execute = async_return(MagicMock())
    session.commit = async_return(None)
    
    await cart_repository.delete_all_carts()

    assert session.execute.called
    assert session.commit.called