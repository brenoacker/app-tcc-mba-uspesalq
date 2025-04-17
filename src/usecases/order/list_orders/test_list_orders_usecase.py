import random
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from usecases.order.list_orders.list_orders_dto import (ListOrdersInputDto)
from usecases.order.list_orders.list_orders_usecase import ListOrdersUseCase


@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def list_orders_usecase(order_repository):
    return ListOrdersUseCase(order_repository)

def test_list_orders_success(list_orders_usecase, order_repository):
    user_id = uuid4()
    order_id = uuid4()
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    order_repository.list_orders.return_value = [order]
    
    input_dto = ListOrdersInputDto(user_id=user_id)
    
    output_dto = list_orders_usecase.execute(input=input_dto)
    
    assert len(output_dto.orders) == 1
    assert output_dto.orders[0].id == order_id
    assert output_dto.orders[0].user_id == user_id
    assert output_dto.orders[0].type == OrderType.IN_STORE
    assert output_dto.orders[0].status == OrderStatus.PENDING
    order_repository.list_orders.assert_called_once_with(user_id=user_id)

def test_list_orders_empty(list_orders_usecase, order_repository):
    user_id = uuid4()
    order_repository.list_orders.return_value = []
    
    input_dto = ListOrdersInputDto(user_id=user_id)
    
    output_dto = list_orders_usecase.execute(input=input_dto)
    
    assert len(output_dto.orders) == 0
    order_repository.list_orders.assert_called_once_with(user_id=user_id)