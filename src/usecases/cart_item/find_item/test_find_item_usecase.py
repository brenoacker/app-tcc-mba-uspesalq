import random
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.cart_item.cart_item_entity import CartItem
from usecases.cart_item.find_item.find_item_dto import (FindItemInputDto,
                                                        FindItemOutputDto)
from usecases.cart_item.find_item.find_item_usecase import FindItemUseCase


@pytest.fixture
def cart_item_repository():
    return Mock()

@pytest.fixture
def find_item_usecase(cart_item_repository):
    return FindItemUseCase(cart_item_repository)

def test_find_item_success(find_item_usecase, cart_item_repository):
    item_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,100)
    cart_item_repository.find_item.return_value = CartItem(id=item_id, cart_id=cart_id, product_id=product_id, quantity=2)
    
    input_dto = FindItemInputDto(id=item_id)
    
    output_dto = find_item_usecase.execute(input=input_dto)
    
    assert output_dto.id == item_id
    assert output_dto.cart_id == cart_id
    assert output_dto.product_id == product_id
    assert output_dto.quantity == 2
    cart_item_repository.find_item.assert_called_once_with(item_id=item_id)

def test_find_item_not_found(find_item_usecase, cart_item_repository):
    item_id = uuid4()
    cart_item_repository.find_item.return_value = None
    
    input_dto = FindItemInputDto(id=item_id)
    
    with pytest.raises(ValueError) as excinfo:
        find_item_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Cart item with id '{item_id}' not found"
    cart_item_repository.find_item.assert_called_once_with(item_id=item_id)