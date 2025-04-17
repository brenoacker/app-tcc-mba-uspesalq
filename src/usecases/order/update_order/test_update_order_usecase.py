import random
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest

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

def test_update_order_success(update_order_usecase, order_repository):
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    order_repository.find_order.return_value = order
    order_repository.update_order.return_value = order
    
    input_dto = UpdateOrderInputDto(id=order_id, user_id=user_id, cart_id=cart_id, type=OrderType.IN_STORE, status=OrderStatus.PENDING, total_price=100.0, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    
    output_dto = update_order_usecase.execute(input=input_dto)
    
    assert output_dto.id == order_id
    assert output_dto.user_id == user_id
    assert output_dto.type == OrderType.IN_STORE
    assert output_dto.status == OrderStatus.PENDING
    order_repository.find_order.assert_called_once_with(order_id=order_id, user_id=user_id)
    order_repository.update_order.assert_called_once()

def test_update_order_not_found(update_order_usecase, order_repository):
    order_id = uuid4()
    order_repository.find_order.return_value = None
    cart_id = uuid4()
    user_id = uuid4()
    
    input_dto = UpdateOrderInputDto(id=order_id, user_id=user_id, cart_id=cart_id, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100), total_price=100.0)
    
    with pytest.raises(ValueError) as excinfo:
        update_order_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Order with id '{order_id}' not found"
    order_repository.find_order.assert_called_once_with(order_id=order_id, user_id=user_id)
    order_repository.update_order.assert_not_called()

def test_update_order_not_updated(update_order_usecase, order_repository):
    order_id = uuid4()
    user_id = uuid4()
    cart_id = uuid4()
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    order_repository.find_order.return_value = order
    order_repository.update_order.return_value = None
    
    input_dto = UpdateOrderInputDto(id=order_id, user_id=user_id, cart_id=cart_id, type=OrderType.IN_STORE, status=OrderStatus.PENDING, total_price=100.0, created_at=datetime.now(), updated_at=datetime.now(), offer_id=random.randint(1,100))
    
    with pytest.raises(ValueError) as excinfo:
        update_order_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Order with id '{order_id}' not updated"
    order_repository.find_order.assert_called_once_with(order_id=order_id, user_id=user_id)
    order_repository.update_order.assert_called_once()