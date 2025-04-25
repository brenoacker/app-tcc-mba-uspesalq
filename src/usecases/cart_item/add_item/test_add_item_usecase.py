import random
from unittest.mock import AsyncMock, MagicMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.cart_item.cart_item_entity import CartItem
from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.cart_item.add_item.add_item_dto import AddItemInputDto
from usecases.cart_item.add_item.add_item_usecase import AddItemUseCase
from usecases.cart_item.update_item.update_item_dto import UpdateItemOutputDto
from usecases.cart_item.update_item.update_item_usecase import \
    UpdateItemUseCase


@pytest.fixture
def cart_item_repository():
    return AsyncMock()

@pytest.fixture
def product_repository():
    return AsyncMock()

@pytest.fixture
def add_item_usecase(cart_item_repository, product_repository):
    return AddItemUseCase(cart_item_repository, product_repository)

@pytest.mark.asyncio
async def test_add_item_success(add_item_usecase, cart_item_repository, product_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,100)
    product = Product(id=product_id, name="Test Product", price=50.0, category=ProductCategory.BURGER)
    product_repository.find_product = async_return(product)
    cart_item_repository.find_item = async_return(None)
    cart_item_repository.add_item = async_return(None)
    
    input_dto = AddItemInputDto(product_id=product_id, quantity=2)
    
    # Substituindo run_async por await
    output_dto = await add_item_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    
    assert output_dto.product_id == product_id
    assert output_dto.quantity == 2
    # Fixing the assertion to match the expected parameter
    cart_item_repository.add_item.assert_awaited_once()

@pytest.mark.asyncio
async def test_add_item_product_not_found(add_item_usecase, product_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_repository.find_product = async_return(None)
    product_id = random.randint(1,100)
    input_dto = AddItemInputDto(product_id=product_id, quantity=2)
    
    with pytest.raises(ValueError) as excinfo:
        # Substituindo run_async por await
        await add_item_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    assert str(excinfo.value) == f"Product with code '{product_id}' not found"
    # Fixing the assertion to match the expected parameter
    product_repository.find_product.assert_awaited_once()

@pytest.mark.asyncio
async def test_add_item_update_existing_item(add_item_usecase, cart_item_repository, product_repository):
    user_id = uuid4()
    cart_id = uuid4()
    item_id = uuid4()
    product_id = random.randint(1,100)
    product = Product(id=product_id, name="Test Product", price=50.0, category=ProductCategory.BURGER)
    product_repository.find_product = async_return(product)
    existing_cart_item = CartItem(id=item_id, cart_id=cart_id, product_id=product_id, quantity=1)
    cart_item_repository.find_item = async_return(existing_cart_item)
    
    input_dto = AddItemInputDto(product_id=product_id, quantity=2)

    # Criando um resultado simulado para o UpdateItemUseCase
    updated_item = UpdateItemOutputDto(id=item_id, cart_id=cart_id, product_id=product_id, quantity=3)
    
    # Mock assíncrono para o método execute da classe UpdateItemUseCase
    update_mock = AsyncMock()
    update_mock.return_value = updated_item
    
    # Aplicando o patch no método execute
    with patch('usecases.cart_item.update_item.update_item_usecase.UpdateItemUseCase.execute', update_mock):
        # Substituindo run_async por await
        output_dto = await add_item_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    
    assert output_dto.product_id == product_id
    assert output_dto.quantity == 3
    assert update_mock.await_count > 0
    assert cart_item_repository.add_item.called == False
