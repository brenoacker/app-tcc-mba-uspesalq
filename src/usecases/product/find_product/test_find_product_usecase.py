import random
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.product.find_product.find_product_dto import FindProductInputDto
from usecases.product.find_product.find_product_usecase import \
    FindProductUsecase


@pytest.fixture
def product_repository():
    repo = Mock()
    repo.find_product = AsyncMock()
    return repo

@pytest.fixture
def find_product_usecase(product_repository):
    return FindProductUsecase(product_repository)

@pytest.mark.asyncio
async def test_find_product_success(find_product_usecase, product_repository):
    product_id = random.randint(1,10)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.DESSERT
    product = Product(id=product_id, name=product_name, price=product_price, category=product_category)
    product_repository.find_product = async_return(product)
    
    input_dto = FindProductInputDto(id=product_id)
    
    output_dto = await find_product_usecase.execute(input=input_dto)
    
    assert output_dto.id == product_id
    assert output_dto.name == product_name
    assert output_dto.price == product_price
    assert output_dto.category == product_category
    product_repository.find_product.assert_awaited_once_with(product_id=product_id)

@pytest.mark.asyncio
async def test_find_product_not_found(find_product_usecase, product_repository):
    product_id = random.randint(1,10)
    product_repository.find_product = async_return(None)
    
    input_dto = FindProductInputDto(id=product_id)
    
    with pytest.raises(ValueError) as excinfo:
        await find_product_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Product with id '{product_id}' not found"
    product_repository.find_product.assert_awaited_once_with(product_id=product_id)