import random
from unittest.mock import Mock

import pytest

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.product.add_product.add_product_dto import (AddProductInputDto)
from usecases.product.add_product.add_product_usecase import AddProductUseCase


@pytest.fixture
def product_repository():
    return Mock()

@pytest.fixture
def add_product_usecase(product_repository):
    return AddProductUseCase(product_repository)

def test_add_product_success(add_product_usecase, product_repository):
    product_id = random.randint(1,100)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.BURGER
    product_repository.find_product_by_name.return_value = None
    product_repository.find_product.return_value = None
    product_repository.add_product.return_value = Product(id=product_id, name=product_name, price=product_price, category=product_category)
    
    input_dto = AddProductInputDto(id=product_id, name=product_name, price=product_price, category=product_category.value)
    
    output_dto = add_product_usecase.execute(input=input_dto)
    
    assert output_dto.id == product_id
    assert output_dto.name == product_name
    assert output_dto.price == product_price
    assert output_dto.category == product_category
    product_repository.find_product_by_name.assert_called_once_with(name=product_name)
    product_repository.find_product.assert_called_once_with(product_id=product_id)
    product_repository.add_product.assert_called_once()

def test_add_product_name_already_registered(add_product_usecase, product_repository):
    product_id = random.randint(1,100)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.BURGER
    product_repository.find_product_by_name.return_value = Product(id=product_id, name=product_name, price=product_price, category=product_category)
    
    input_dto = AddProductInputDto(id=product_id, name=product_name, price=product_price, category=product_category.value)
    
    with pytest.raises(ValueError) as excinfo:
        add_product_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Product with '{product_name}' name already registered"
    product_repository.find_product_by_name.assert_called_once_with(name=product_name)
    product_repository.find_product.assert_not_called()
    product_repository.add_product.assert_not_called()

def test_add_product_id_already_registered(add_product_usecase, product_repository):
    product_id = random.randint(1,100)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.BURGER
    product_repository.find_product_by_name.return_value = None
    product_repository.find_product.return_value = Product(id=product_id, name=product_name, price=product_price, category=product_category)
    
    input_dto = AddProductInputDto(id=product_id, name=product_name, price=product_price, category=product_category.value)
    
    with pytest.raises(ValueError) as excinfo:
        add_product_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Product id '{product_id}' already registered"
    product_repository.find_product_by_name.assert_called_once_with(name=product_name)
    product_repository.find_product.assert_called_once_with(product_id=product_id)
    product_repository.add_product.assert_not_called()