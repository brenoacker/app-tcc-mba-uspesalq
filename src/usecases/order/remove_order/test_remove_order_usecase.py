from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from usecases.order.remove_order.remove_order_dto import RemoveOrderInputDto
from usecases.order.remove_order.remove_order_usecase import RemoveOrderUseCase


@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def remove_order_usecase(order_repository):
    return RemoveOrderUseCase(order_repository)

@pytest.mark.asyncio
async def test_remove_order_success(remove_order_usecase, order_repository):
    order_id = uuid4()
    order_repository.remove_order = async_return(order_id)
    
    input_dto = RemoveOrderInputDto(id=order_id)
    
    output_dto = await remove_order_usecase.execute(input=input_dto)
    
    assert output_dto.id == order_id
    order_repository.remove_order.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_remove_order_not_found(remove_order_usecase, order_repository):
    order_id = uuid4()
    order_repository.remove_order = async_return(None)
    
    input_dto = RemoveOrderInputDto(id=order_id)
    
    with pytest.raises(ValueError) as excinfo:
        run_async(remove_order_usecase.execute(input=input_dto))
    assert str(excinfo.value) == f"Order with id '{order_id}' not found"
    order_repository.remove_order.assert_awaited_once_with()