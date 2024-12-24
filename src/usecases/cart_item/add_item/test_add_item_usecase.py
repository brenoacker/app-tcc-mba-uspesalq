import random
from unittest.mock import Mock, patch
from uuid import uuid4

import pytest

from domain.cart_item.cart_item_entity import CartItem
from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.cart_item.add_item.add_item_dto import (AddItemInputDto,
                                                      AddItemOutputDto)
from usecases.cart_item.add_item.add_item_usecase import AddItemUseCase
from usecases.cart_item.update_item.update_item_dto import (
    UpdateItemInputDto, UpdateItemOutputDto)
from usecases.cart_item.update_item.update_item_usecase import \
    UpdateItemUseCase


@pytest.fixture
def cart_item_repository():
    return Mock()

@pytest.fixture
def product_repository():
    return Mock()

@pytest.fixture
def add_item_usecase(cart_item_repository, product_repository):
    return AddItemUseCase(cart_item_repository, product_repository)

def test_add_item_success(add_item_usecase, cart_item_repository, product_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,100)
    product_repository.find_product.return_value = Product(id=product_id, name="Test Product", price=50.0, category=ProductCategory.BURGER)
    cart_item_repository.find_item.return_value = None
    
    input_dto = AddItemInputDto(product_id=product_id, quantity=2)
    
    output_dto = add_item_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    
    assert output_dto.product_id == product_id
    assert output_dto.quantity == 2
    cart_item_repository.add_item.assert_called_once()

def test_add_item_product_not_found(add_item_usecase, product_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_repository.find_product.return_value = None
    product_id = random.randint(1,100)
    input_dto = AddItemInputDto(product_id=product_id, quantity=2)
    
    with pytest.raises(ValueError) as excinfo:
        add_item_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    assert str(excinfo.value) == f"Product with code '{product_id}' not found"
    product_repository.find_product.assert_called_once_with(product_id=product_id)

def test_add_item_update_existing_item(add_item_usecase, cart_item_repository, product_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,100)
    product_repository.find_product.return_value = Product(id=product_id, name="Test Product", price=50.0, category=ProductCategory.BURGER)
    existing_cart_item = CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=1)
    cart_item_repository.find_item.return_value = existing_cart_item
    
    input_dto = AddItemInputDto(product_id=product_id, quantity=2)

    with patch.object(UpdateItemUseCase, 'execute', return_value=UpdateItemOutputDto(id=existing_cart_item.id, cart_id=cart_id, product_id=product_id, quantity=3)) as mock_update:
        output_dto = add_item_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    
    assert output_dto.product_id == product_id
    assert output_dto.quantity == 3
    mock_update.assert_called_once()
    cart_item_repository.add_item.assert_not_called()
