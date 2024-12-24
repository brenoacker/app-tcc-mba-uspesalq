import random
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from usecases.order.find_order.find_order_dto import (FindOrderInputDto,
                                                      FindOrderOutputDto)
from usecases.order.find_order.find_order_usecase import FindOrderUseCase


@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def find_order_usecase(order_repository):
    return FindOrderUseCase(order_repository)

def test_find_order_success(find_order_usecase, order_repository):
    order_id = uuid4()
    user_id = uuid4()
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.DRIVE_THRU, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    order_repository.find_order.return_value = FindOrderOutputDto(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=order.total_price, status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)
    
    input_dto = FindOrderInputDto(id=order_id)
    
    output_dto = find_order_usecase.execute(input=input_dto)
    
    assert output_dto.id == order_id
    assert output_dto.user_id == user_id
    assert output_dto.type == OrderType.DRIVE_THRU
    assert output_dto.status == OrderStatus.PENDING
    order_repository.find_order.assert_called_once_with(order_id=order_id)

def test_find_order_not_found(find_order_usecase, order_repository):
    order_id = uuid4()
    order_repository.find_order.return_value = None
    
    input_dto = FindOrderInputDto(id=order_id)
    
    with pytest.raises(ValueError) as excinfo:
        find_order_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Order with id '{order_id}' not found"
    order_repository.find_order.assert_called_once_with(order_id=order_id)