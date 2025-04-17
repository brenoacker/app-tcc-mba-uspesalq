import uuid
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.cart.cart_entity import Cart
from domain.cart_item.cart_item_entity import CartItem
from usecases.cart.find_cart_items.find_cart_items_dto import (
    FindCartItemDto, FindCartItemsInputDto, FindCartItemsOutputDto)
from usecases.cart.find_cart_items.find_cart_items_usecase import \
    FindCartItemsUseCase


@pytest.fixture
def cart_repository():
    return AsyncMock()

@pytest.fixture
def cart_item_repository():
    return AsyncMock()

@pytest.fixture
def find_cart_items_usecase(cart_repository, cart_item_repository):
    return FindCartItemsUseCase(cart_repository, cart_item_repository)

@pytest.mark.asyncio
async def test_find_cart_items_success(find_cart_items_usecase, cart_repository, cart_item_repository):
    user_id = uuid4()
    cart_id = uuid4()
    cart = Cart(id=cart_id, user_id=user_id, total_price=100.0)
    cart_repository.find_cart = async_return(cart)

    cart_item_id_1 = uuid4()
    cart_item_id_2 = uuid4()
    cart_items = [
        CartItem(id=cart_item_id_1, cart_id=cart_id, product_id=1, quantity=2),
        CartItem(id=cart_item_id_2, cart_id=cart_id, product_id=2, quantity=3)
    ]
    cart_item_repository.find_items_by_cart_id = async_return(cart_items)

    input_dto = FindCartItemsInputDto(cart_id=cart_id, user_id=user_id)

    output_dto = await find_cart_items_usecase.execute(input=input_dto)

    assert len(output_dto.items) == 2
    assert output_dto.items[0].id == cart_item_id_1
    assert output_dto.items[0].product_id == 1
    assert output_dto.items[0].quantity == 2
    assert output_dto.items[1].id == cart_item_id_2
    assert output_dto.items[1].product_id == 2
    assert output_dto.items[1].quantity == 3
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)
    cart_item_repository.find_items_by_cart_id.assert_awaited_once_with(cart_id=cart_id)

@pytest.mark.asyncio
async def test_find_cart_items_cart_not_found(find_cart_items_usecase, cart_repository):
    user_id = uuid4()
    cart_id = uuid4()
    cart_repository.find_cart = async_return(None)

    input_dto = FindCartItemsInputDto(cart_id=cart_id, user_id=user_id)

    with pytest.raises(ValueError) as excinfo:
        await find_cart_items_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Cart not found: {cart_id}"
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)