import random
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.product.find_product.find_product_dto import (
    FindProductInputDto, FindProductOutputDto)
from usecases.product.find_product.find_product_usecase import \
    FindProductUsecase


@pytest.fixture
def product_repository():
    return Mock()

@pytest.fixture
def find_product_usecase(product_repository):
    return FindProductUsecase(product_repository)

def test_find_product_success(find_product_usecase, product_repository):
    product_id = random.randint(1,10)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.DESSERT
    product = Product(id=product_id, name=product_name, price=product_price, category=product_category)
    product_repository.find_product.return_value = product
    
    input_dto = FindProductInputDto(id=product_id)
    
    output_dto = find_product_usecase.execute(input=input_dto)
    
    assert output_dto.id == product_id
    assert output_dto.name == product_name
    assert output_dto.price == product_price
    assert output_dto.category == product_category
    product_repository.find_product.assert_called_once_with(product_id=product_id)

def test_find_product_not_found(find_product_usecase, product_repository):
    product_id = random.randint(1,10)
    product_repository.find_product.return_value = None
    
    input_dto = FindProductInputDto(id=product_id)
    
    with pytest.raises(ValueError) as excinfo:
        find_product_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Product with id '{product_id}' not found"
    product_repository.find_product.assert_called_once_with(product_id=product_id)