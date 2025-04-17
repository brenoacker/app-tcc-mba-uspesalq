import random
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from domain.cart_item.cart_item_entity import CartItem
from usecases.cart_item.remove_item.remove_item_dto import (
    RemoveItemInputDto, RemoveItemOutputDto)
from usecases.cart_item.remove_item.remove_item_usecase import \
    RemoveItemUseCase


@pytest.fixture
def cart_item_repository():
    return AsyncMock()

@pytest.fixture
def remove_item_usecase(cart_item_repository):
    return RemoveItemUseCase(cart_item_repository)

@pytest.mark.asyncio
async def test_remove_item_success(remove_item_usecase, cart_item_repository):
    item_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,100)
    cart_item_repository.find_item = async_return(CartItem(id=item_id, cart_id=cart_id, product_id=product_id, quantity=2))
    
    input_dto = RemoveItemInputDto(id=item_id)
    
    output_dto = await remove_item_usecase.execute(input=input_dto)
    
    assert output_dto.id == item_id
    assert output_dto.cart_id == cart_id
    assert output_dto.product_id == product_id
    assert output_dto.quantity == 2
    cart_item_repository.find_item.assert_awaited_once_with()
    cart_item_repository.remove_item.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_remove_item_not_found(remove_item_usecase, cart_item_repository):
    item_id = uuid4()
    cart_item_repository.find_item = async_return(None)
    
    input_dto = RemoveItemInputDto(id=item_id)
    
    with pytest.raises(ValueError) as excinfo:
        run_async(remove_item_usecase.execute(input=input_dto))
    assert str(excinfo.value) == f"Cart Item with id '{item_id}' not found"
    cart_item_repository.find_item.assert_awaited_once_with()
    assert cart_item_repository.remove_item.called == False