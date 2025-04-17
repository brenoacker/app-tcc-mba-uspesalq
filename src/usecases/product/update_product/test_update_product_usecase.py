import random
from unittest.mock import Mock

import pytest

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.product.update_product.update_product_dto import (
    UpdateProductInputDto)
from usecases.product.update_product.update_product_usecase import \
    UpdateProductUseCase


@pytest.fixture
def product_repository():
    return Mock()

@pytest.fixture
def update_product_usecase(product_repository):
    return UpdateProductUseCase(product_repository)

def test_update_product_success(update_product_usecase, product_repository):
    product_id = random.randint(1,10)
    product_name = "Updated Product"
    product_price = 150.0
    product_category = ProductCategory.BURGER
    product = Product(id=product_id, name=product_name, price=product_price, category=product_category)
    product_repository.find_product.return_value = product
    
    input_dto = UpdateProductInputDto(id=product_id, name=product_name, price=product_price, category=product_category)
    
    output_dto = update_product_usecase.execute(input=input_dto)
    
    assert output_dto.id == product_id
    assert output_dto.name == product_name
    assert output_dto.price == product_price
    assert output_dto.category == product_category
    product_repository.find_product.assert_called_once_with(product_id=product_id)
    product_repository.update_product.assert_called_once_with(product=product)

def test_update_product_not_found(update_product_usecase, product_repository):
    product_id = random.randint(1,10)
    product_repository.find_product.return_value = None
    
    input_dto = UpdateProductInputDto(id=product_id, name="Updated Product", price=150.0, category=ProductCategory.BURGER)
    
    with pytest.raises(ValueError) as excinfo:
        update_product_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Product with id '{product_id}' not found"
    product_repository.find_product.assert_called_once_with(product_id=product_id)
    product_repository.update_product.assert_not_called()