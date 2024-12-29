import random
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.cart_item.cart_item_entity import CartItem
from usecases.cart_item.update_item.update_item_dto import (
    UpdateItemInputDto)
from usecases.cart_item.update_item.update_item_usecase import \
    UpdateItemUseCase


@pytest.fixture
def cart_item_repository():
    return Mock()

@pytest.fixture
def update_item_usecase(cart_item_repository):
    return UpdateItemUseCase(cart_item_repository)

def test_update_item_success(update_item_usecase, cart_item_repository):
    item_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,100)
    cart_item_repository.find_item.return_value = CartItem(id=item_id, cart_id=cart_id, product_id=product_id, quantity=2)
    
    input_dto = UpdateItemInputDto(quantity=5)
    
    output_dto = update_item_usecase.execute(cart_item_id=item_id, input=input_dto)
    
    assert output_dto.id == item_id
    assert output_dto.cart_id == cart_id
    assert output_dto.product_id == product_id
    assert output_dto.quantity == 5
    cart_item_repository.find_item.assert_called_once_with(item_id=item_id)
    cart_item_repository.update_item.assert_called_once()

def test_update_item_not_found(update_item_usecase, cart_item_repository):
    item_id = uuid4()
    cart_item_repository.find_item.return_value = None
    
    input_dto = UpdateItemInputDto(quantity=5)
    
    with pytest.raises(ValueError) as excinfo:
        update_item_usecase.execute(cart_item_id=item_id, input=input_dto)
    assert str(excinfo.value) == f"Cart item with id '{item_id}' not found"
    cart_item_repository.find_item.assert_called_once_with(item_id=item_id)
    cart_item_repository.update_item.assert_not_called()