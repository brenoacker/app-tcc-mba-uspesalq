import random
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.cart_item.cart_item_entity import CartItem
from usecases.cart_item.list_items_by_user.list_items_by_user_dto import (
    ListItemsByUserInputDto)
from usecases.cart_item.list_items_by_user.list_items_by_user_usecase import \
    ListItemsByUserUseCase


@pytest.fixture
def cart_item_repository():
    return Mock()

@pytest.fixture
def list_items_by_user_usecase(cart_item_repository):
    return ListItemsByUserUseCase(cart_item_repository)

def test_list_items_by_user_success(list_items_by_user_usecase, cart_item_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,100)
    cart_item_repository.list_items_by_user.return_value = [
        CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=2),
        CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=3)
    ]
    
    input_dto = ListItemsByUserInputDto(user_id=user_id)
    
    output_dto = list_items_by_user_usecase.execute(input=input_dto)
    
    assert len(output_dto.items) == 2
    assert output_dto.items[0].quantity == 2
    assert output_dto.items[1].quantity == 3
    cart_item_repository.list_items_by_user.assert_called_once_with(user_id=user_id)

def test_list_items_by_user_empty(list_items_by_user_usecase, cart_item_repository):
    user_id = uuid4()
    cart_item_repository.list_items_by_user.return_value = []
    
    input_dto = ListItemsByUserInputDto(user_id=user_id)
    
    output_dto = list_items_by_user_usecase.execute(input=input_dto)
    
    assert len(output_dto.items) == 0
    cart_item_repository.list_items_by_user.assert_called_once_with(user_id=user_id)