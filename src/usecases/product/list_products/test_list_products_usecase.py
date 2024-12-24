import random
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.product.list_products.list_products_dto import \
    ListProductsOutputDto
from usecases.product.list_products.list_products_usecase import \
    ListProductsUseCase


@pytest.fixture
def product_repository():
    return Mock()

@pytest.fixture
def list_products_usecase(product_repository):
    return ListProductsUseCase(product_repository)

def test_list_products_success(list_products_usecase, product_repository):
    product_id = random.randint(1,10)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.SIDE_DISH
    product = Product(id=product_id, name=product_name, price=product_price, category=product_category)
    product_repository.list_products.return_value = [product]
    
    output_dto = list_products_usecase.execute()
    
    assert len(output_dto.products) == 1
    assert output_dto.products[0].id == product_id
    assert output_dto.products[0].name == product_name
    assert output_dto.products[0].price == product_price
    assert output_dto.products[0].category == product_category
    product_repository.list_products.assert_called_once()

def test_list_products_empty(list_products_usecase, product_repository):
    product_repository.list_products.return_value = []
    
    output_dto = list_products_usecase.execute()
    
    assert len(output_dto.products) == 0
    product_repository.list_products.assert_called_once()