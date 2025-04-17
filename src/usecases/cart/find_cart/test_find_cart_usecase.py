import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.cart.cart_entity import Cart
from usecases.cart.find_cart.find_cart_dto import (FindCartInputDto,
                                                   FindCartOutputDto)
from usecases.cart.find_cart.find_cart_usecase import FindCartUseCase


@pytest.fixture
def cart_repository():
    repo = Mock()
    repo.find_cart = AsyncMock()
    return repo

@pytest.fixture
def find_cart_usecase(cart_repository):
    return FindCartUseCase(cart_repository)

@pytest.mark.asyncio
async def test_find_cart_success(find_cart_usecase, cart_repository):
    cart_id = uuid.uuid4()
    user_id = uuid.uuid4()
    cart_repository.find_cart = async_return(Cart(id=cart_id, user_id=user_id, total_price=100.0))
    
    input_dto = FindCartInputDto(id=cart_id, user_id=user_id)
    
    output_dto = await find_cart_usecase.execute(input=input_dto)
    
    assert output_dto.id == cart_id
    assert output_dto.user_id == user_id
    assert output_dto.total_price == 100.0
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)

@pytest.mark.asyncio
async def test_find_cart_not_found(find_cart_usecase, cart_repository):
    cart_id = uuid.uuid4()
    user_id = uuid.uuid4()
    cart_repository.find_cart = async_return(None)
    
    input_dto = FindCartInputDto(id=cart_id, user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        await find_cart_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Cart with id '{cart_id}' not found"
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)