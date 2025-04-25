import random
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.cart_item.cart_item_entity import CartItem
from usecases.cart_item.list_items_by_user.list_items_by_user_dto import \
    ListItemsByUserInputDto
from usecases.cart_item.list_items_by_user.list_items_by_user_usecase import \
    ListItemsByUserUseCase


@pytest.fixture
def cart_item_repository():
    return AsyncMock()

@pytest.fixture
def list_items_by_user_usecase(cart_item_repository):
    return ListItemsByUserUseCase(cart_item_repository)

@pytest.mark.asyncio
async def test_list_items_by_user_success(list_items_by_user_usecase, cart_item_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,100)
    cart_item_repository.list_items_by_user = async_return([
        CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=2),
        CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=3)
    ])
    
    input_dto = ListItemsByUserInputDto(user_id=user_id)
    
    output_dto = await list_items_by_user_usecase.execute(input=input_dto)
    
    assert len(output_dto.items) == 2
    assert output_dto.items[0].quantity == 2
    assert output_dto.items[1].quantity == 3
    cart_item_repository.list_items_by_user.assert_awaited_once()

@pytest.mark.asyncio
async def test_list_items_by_user_empty(list_items_by_user_usecase, cart_item_repository):
    user_id = uuid4()
    cart_item_repository.list_items_by_user = async_return([])
    
    input_dto = ListItemsByUserInputDto(user_id=user_id)
    
    output_dto = await list_items_by_user_usecase.execute(input=input_dto)
    
    assert len(output_dto.items) == 0
    cart_item_repository.list_items_by_user.assert_awaited_once()