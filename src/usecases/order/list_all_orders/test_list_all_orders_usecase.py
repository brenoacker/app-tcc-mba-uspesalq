import random
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from usecases.order.list_all_orders.list_all_orders_dto import (
    ListAllOrderDto, ListAllOrdersOutputDto)
from usecases.order.list_all_orders.list_all_orders_usecase import \
    ListAllOrdersUseCase


@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def list_all_orders_usecase(order_repository):
    return ListAllOrdersUseCase(order_repository)

def test_list_all_orders_success(list_all_orders_usecase, order_repository):
    order_id = uuid4()
    user_id = uuid4()
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    order_repository.list_all_orders.return_value = [order]
    
    output_dto = list_all_orders_usecase.execute()
    
    assert len(output_dto.orders) == 1
    assert output_dto.orders[0].id == order_id
    assert output_dto.orders[0].user_id == user_id
    assert output_dto.orders[0].type == OrderType.IN_STORE
    assert output_dto.orders[0].status == OrderStatus.PENDING
    order_repository.list_all_orders.assert_called_once()

def test_list_all_orders_empty(list_all_orders_usecase, order_repository):
    order_repository.list_all_orders.return_value = []
    
    output_dto = list_all_orders_usecase.execute()
    
    assert len(output_dto.orders) == 0
    order_repository.list_all_orders.assert_called_once()