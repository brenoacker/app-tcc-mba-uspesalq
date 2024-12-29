import random
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.cart_item.cart_item_entity import CartItem
from usecases.cart_item.list_items.list_items_usecase import ListItemsUseCase


@pytest.fixture
def cart_item_repository():
    return Mock()

@pytest.fixture
def list_items_usecase(cart_item_repository):
    return ListItemsUseCase(cart_item_repository)

def test_list_items_success(list_items_usecase, cart_item_repository):
    cart_id = uuid4()
    product_id = random.randint(1,100)
    cart_item_repository.list_items.return_value = [
        CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=2),
        CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=3)
    ]
    
    output_dto = list_items_usecase.execute()
    
    assert len(output_dto.items) == 2
    assert output_dto.items[0].quantity == 2
    assert output_dto.items[1].quantity == 3
    cart_item_repository.list_items.assert_called_once()

def test_list_items_empty(list_items_usecase, cart_item_repository):
    cart_item_repository.list_items.return_value = []
    
    output_dto = list_items_usecase.execute()
    
    assert len(output_dto.items) == 0
    cart_item_repository.list_items.assert_called_once()