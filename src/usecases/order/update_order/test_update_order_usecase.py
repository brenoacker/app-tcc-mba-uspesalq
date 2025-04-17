import random
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from usecases.order.update_order.update_order_dto import UpdateOrderInputDto
from usecases.order.update_order.update_order_usecase import UpdateOrderUseCase


@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def update_order_usecase(order_repository):
    return UpdateOrderUseCase(order_repository)

@pytest.mark.asyncio
async def test_update_order_success(update_order_usecase, order_repository):
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    order_repository.find_order = async_return(order)
    order_repository.update_order = async_return(order)
    
    input_dto = UpdateOrderInputDto(id=order_id, user_id=user_id, cart_id=cart_id, type=OrderType.IN_STORE, status=OrderStatus.PENDING, total_price=100.0, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    
    output_dto = await update_order_usecase.execute(input=input_dto)
    
    assert output_dto.id == order_id
    assert output_dto.user_id == user_id
    assert output_dto.type == OrderType.IN_STORE
    assert output_dto.status == OrderStatus.PENDING
    order_repository.find_order.assert_awaited_once_with()
    order_repository.update_order.await_count == 1

@pytest.mark.asyncio
async def test_update_order_not_found(update_order_usecase, order_repository):
    order_id = uuid4()
    order_repository.find_order = async_return(None)
    cart_id = uuid4()
    
    input_dto = UpdateOrderInputDto(id=order_id, user_id=uuid4(), cart_id=cart_id, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100), total_price=100.0)
    
    with pytest.raises(ValueError) as excinfo:
        run_async(update_order_usecase.execute(input=input_dto))
    assert str(excinfo.value) == f"Order with id '{order_id}' not found"
    order_repository.find_order.assert_awaited_once_with()
    order_repository.update_order.called == False