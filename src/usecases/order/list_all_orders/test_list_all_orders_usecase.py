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
from usecases.order.list_all_orders.list_all_orders_usecase import \
    ListAllOrdersUseCase


@pytest.fixture
def order_repository():
    repo = Mock()
    repo.list_all_orders = AsyncMock()
    return repo

@pytest.fixture
def list_all_orders_usecase(order_repository):
    return ListAllOrdersUseCase(order_repository)

@pytest.mark.asyncio
async def test_list_all_orders_success(list_all_orders_usecase, order_repository):
    order_id = uuid4()
    user_id = uuid4()
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    
    # Atualizando o mock para retornar o formato de resposta correto (dicionário com 'items')
    order_repository.list_all_orders = async_return({
        "items": [order],
        "pagination": {
            "page": 1,
            "page_size": 50,
            "total_count": 1,
            "total_pages": 1
        }
    })
    
    output_dto = await list_all_orders_usecase.execute()
    
    assert len(output_dto.orders) == 1
    assert output_dto.orders[0].id == order_id
    assert output_dto.orders[0].user_id == user_id
    assert output_dto.orders[0].type == OrderType.IN_STORE
    assert output_dto.orders[0].status == OrderStatus.PENDING
    order_repository.list_all_orders.assert_awaited_once()

@pytest.mark.asyncio
async def test_list_all_orders_empty(list_all_orders_usecase, order_repository):
    # Atualizando o mock para retornar o formato de resposta correto (dicionário com 'items' vazio)
    order_repository.list_all_orders = async_return({
        "items": [],
        "pagination": {
            "page": 1,
            "page_size": 50,
            "total_count": 0,
            "total_pages": 0
        }
    })
    
    output_dto = await list_all_orders_usecase.execute()
    
    assert len(output_dto.orders) == 0
    order_repository.list_all_orders.assert_awaited_once()

@pytest.mark.asyncio
async def test_list_all_orders_none(list_all_orders_usecase, order_repository):
    order_repository.list_all_orders = async_return(None)
    
    output_dto = await list_all_orders_usecase.execute()
    
    assert len(output_dto.orders) == 0
    order_repository.list_all_orders.assert_awaited_once()
