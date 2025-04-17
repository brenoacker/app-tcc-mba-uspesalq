from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID, uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.cart.cart_entity import Cart
from usecases.cart.remove_cart.remove_cart_dto import (RemoveCartInputDto,
                                                       RemoveCartOutputDto)
from usecases.cart.remove_cart.remove_cart_usecase import RemoveCartUseCase


@pytest.fixture
def cart_repository():
    repo = Mock()
    repo.find_cart = AsyncMock()
    repo.remove_cart = AsyncMock()
    return repo

@pytest.fixture
def remove_cart_usecase(cart_repository):
    return RemoveCartUseCase(cart_repository)

@pytest.mark.asyncio
async def test_remove_cart_success(remove_cart_usecase, cart_repository):
    cart_id = uuid4()
    user_id = uuid4()
    cart_repository.find_cart = async_return(Cart(id=cart_id, user_id=user_id, total_price=100.0))
    
    input_dto = RemoveCartInputDto(id=cart_id, user_id=user_id)
    
    output_dto = await remove_cart_usecase.execute(input=input_dto)
    
    assert output_dto.id == cart_id
    assert output_dto.user_id == user_id
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)
    cart_repository.remove_cart.assert_awaited_once_with(cart_id=cart_id)

@pytest.mark.asyncio
async def test_remove_cart_not_found(remove_cart_usecase, cart_repository):
    cart_id = uuid4()
    user_id = uuid4()
    cart_repository.find_cart = async_return(None)
    
    input_dto = RemoveCartInputDto(id=cart_id, user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        await remove_cart_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Cart with id '{cart_id}' not found"
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)
    assert not cart_repository.remove_cart.called