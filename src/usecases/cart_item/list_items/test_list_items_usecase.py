import random
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from domain.cart_item.cart_item_entity import CartItem
from usecases.cart_item.list_items.list_items_dto import (ListItemsDto,
                                                          ListItemsOutputDto)
from usecases.cart_item.list_items.list_items_usecase import ListItemsUseCase


@pytest.fixture
def cart_item_repository():
    return AsyncMock()

@pytest.fixture
def list_items_usecase(cart_item_repository):
    return ListItemsUseCase(cart_item_repository)

@pytest.mark.asyncio
async def test_list_items_success(list_items_usecase, cart_item_repository):
    cart_id = uuid4()
    product_id = random.randint(1,100)
    cart_items = [
        CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=2),
        CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=3)
    ]
    cart_item_repository.list_items = async_return(cart_items)
    
    output_dto = await list_items_usecase.execute()
    
    assert len(output_dto.items) == 2
    assert output_dto.items[0].quantity == 2
    assert output_dto.items[1].quantity == 3
    cart_item_repository.list_items.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_list_items_empty(list_items_usecase, cart_item_repository):
    cart_item_repository.list_items = async_return([])
    
    output_dto = await list_items_usecase.execute()
    
    assert len(output_dto.items) == 0
    cart_item_repository.list_items.assert_awaited_once_with()