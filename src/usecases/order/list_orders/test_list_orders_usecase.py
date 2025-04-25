import random
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from usecases.order.list_orders.list_orders_dto import ListOrdersInputDto
from usecases.order.list_orders.list_orders_usecase import ListOrdersUseCase


@pytest.fixture
def order_repository():
    repo = Mock()
    repo.list_orders = AsyncMock()
    return repo

@pytest.fixture
def list_orders_usecase(order_repository):
    return ListOrdersUseCase(order_repository)

@pytest.mark.asyncio
async def test_list_orders_success(list_orders_usecase, order_repository):
    user_id = uuid4()
    order_id = uuid4()
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    order_repository.list_orders = async_return([order])
    
    input_dto = ListOrdersInputDto(user_id=user_id)
    
    output_dto = await list_orders_usecase.execute(input=input_dto)
    
    assert len(output_dto.orders) == 1
    assert output_dto.orders[0].id == order_id
    assert output_dto.orders[0].user_id == user_id
    assert output_dto.orders[0].type == OrderType.IN_STORE
    assert output_dto.orders[0].status == OrderStatus.PENDING
    order_repository.list_orders.await_count == 1

@pytest.mark.asyncio
async def test_list_orders_empty(list_orders_usecase, order_repository):
    user_id = uuid4()
    order_repository.list_orders = async_return([])
    
    input_dto = ListOrdersInputDto(user_id=user_id)
    
    output_dto = await list_orders_usecase.execute(input=input_dto)
    
    assert len(output_dto.orders) == 0
    order_repository.list_orders.await_count == 1