from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from domain.cart.cart_entity import Cart
from usecases.cart.list_carts.list_carts_dto import (ListCartsInputDto,
                                                     ListCartsOutputDto)
from usecases.cart.list_carts.list_carts_usecase import ListCartsUseCase


@pytest.fixture
def cart_repository():
    return Mock()

@pytest.fixture
def list_carts_usecase(cart_repository):
    return ListCartsUseCase(cart_repository)

@pytest.mark.asyncio
async def test_list_carts_success(list_carts_usecase, cart_repository):
    user_id = uuid4()
    cart_id = uuid4()
    carts = [
        Cart(id=cart_id, user_id=user_id, total_price=100.0),
        Cart(id=uuid4(), user_id=user_id, total_price=200.0)
    ]
    cart_repository.list_carts = async_return(carts)
    
    input_dto = ListCartsInputDto(user_id=user_id)
    
    output_dto = await list_carts_usecase.execute(input=input_dto)
    
    assert len(output_dto.carts) == 2
    assert output_dto.carts[0].id == cart_id
    assert output_dto.carts[0].total_price == 100.0
    assert output_dto.carts[1].total_price == 200.0
    cart_repository.list_carts.assert_awaited_once_with(user_id=user_id)

@pytest.mark.asyncio
async def test_list_carts_empty(list_carts_usecase, cart_repository):
    user_id = uuid4()
    cart_repository.list_carts = async_return(None)
    
    input_dto = ListCartsInputDto(user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        await list_carts_usecase.execute(input=input_dto)
    assert str(excinfo.value) == "No carts found"
    cart_repository.list_carts.assert_called_once_with(user_id=user_id)