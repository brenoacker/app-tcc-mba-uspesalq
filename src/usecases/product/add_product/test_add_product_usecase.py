import random
from unittest.mock import AsyncMock, Mock, patch

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.product.add_product.add_product_dto import (AddProductInputDto,
                                                          AddProductOutputDto)
from usecases.product.add_product.add_product_usecase import AddProductUseCase


@pytest.fixture
def product_repository():
    repo = Mock()
    repo.find_product = AsyncMock()
    repo.find_product_by_name = AsyncMock()
    repo.add_product = AsyncMock()
    return repo

@pytest.fixture
def add_product_usecase(product_repository):
    return AddProductUseCase(product_repository)

@pytest.mark.asyncio
async def test_add_product_success(add_product_usecase, product_repository):
    product_id = random.randint(1,100)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.BURGER
    product_repository.find_product_by_name = async_return(None)
    product_repository.find_product = async_return(None)
    product_repository.add_product = async_return(Product(id=product_id, name=product_name, price=product_price, category=product_category))

    input_dto = AddProductInputDto(id=product_id, name=product_name, price=product_price, category=product_category.value)

    output_dto = await add_product_usecase.execute(input=input_dto)

    assert output_dto.id == product_id
    assert output_dto.name == product_name
    assert output_dto.price == product_price
    assert output_dto.category == product_category
    product_repository.find_product_by_name.assert_awaited_once_with(name=product_name)
    product_repository.find_product.assert_awaited_once_with(product_id=product_id)
    assert product_repository.add_product.await_count == 1

@pytest.mark.asyncio
async def test_add_product_name_already_registered(add_product_usecase, product_repository):
    product_id = random.randint(1,100)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.BURGER
    product_repository.find_product_by_name = async_return(Product(id=product_id, name=product_name, price=product_price, category=product_category))

    input_dto = AddProductInputDto(id=product_id, name=product_name, price=product_price, category=product_category.value)

    with pytest.raises(ValueError) as excinfo:
        await add_product_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Product with name '{product_name}' already registered"
    product_repository.find_product_by_name.assert_awaited_once_with(name=product_name)
    assert not product_repository.add_product.called

@pytest.mark.asyncio
async def test_add_product_id_already_registered(add_product_usecase, product_repository):
    product_id = random.randint(1,100)
    product_name = "Test Product"
    product_price = 100.0
    product_category = ProductCategory.BURGER
    product_repository.find_product_by_name = async_return(None)
    product_repository.find_product = async_return(Product(id=product_id, name=product_name, price=product_price, category=product_category))

    input_dto = AddProductInputDto(id=product_id, name=product_name, price=product_price, category=product_category.value)

    with pytest.raises(ValueError) as excinfo:
        await add_product_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Product with id '{product_id}' already registered"
    product_repository.find_product_by_name.assert_awaited_once_with(name=product_name)
    product_repository.find_product.assert_awaited_once_with(product_id=product_id)
    assert not product_repository.add_product.called