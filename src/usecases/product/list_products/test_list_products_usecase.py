import random
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.product.list_products.list_products_usecase import \
    ListProductsUseCase


@pytest.fixture
def product_repository():
    repo = Mock()
    repo.list_products = AsyncMock()
    return repo

@pytest.fixture
def list_products_usecase(product_repository):
    return ListProductsUseCase(product_repository)

@pytest.mark.asyncio
async def test_list_products_success(list_products_usecase, product_repository):
    product_id = random.randint(1,10)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.SIDE_DISH
    product = Product(id=product_id, name=product_name, price=product_price, category=product_category)
    product_repository.list_products = async_return([product])
    
    output_dto = await list_products_usecase.execute()
    
    assert len(output_dto.products) == 1
    assert output_dto.products[0].id == product_id
    assert output_dto.products[0].name == product_name
    assert output_dto.products[0].price == product_price
    assert output_dto.products[0].category == product_category
    product_repository.list_products.await_count == 1

@pytest.mark.asyncio
async def test_list_products_empty(list_products_usecase, product_repository):
    product_repository.list_products = async_return([])
    
    output_dto = await list_products_usecase.execute()
    
    assert len(output_dto.products) == 0
    product_repository.list_products.await_count == 1
