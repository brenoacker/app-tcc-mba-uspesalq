import random
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.cart.cart_entity import Cart
from domain.cart_item.cart_item_entity import CartItem
from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from usecases.cart.update_cart.update_cart_dto import (UpdateCartInputDto,
                                                       UpdateCartItemDto,
                                                       UpdateCartOutputDto)
from usecases.cart.update_cart.update_cart_usecase import UpdateCartUseCase


@pytest.fixture
def cart_repository():
    repo = Mock()
    repo.find_cart = AsyncMock()
    repo.find_items_by_cart_id = AsyncMock()
    return repo

@pytest.fixture
def cart_item_repository():
    return AsyncMock()

@pytest.fixture
def product_repository():
    return AsyncMock()

@pytest.fixture
def update_cart_usecase(cart_repository, cart_item_repository, product_repository):
    return UpdateCartUseCase(cart_repository, cart_item_repository, product_repository)

@pytest.mark.asyncio
async def test_update_cart_success(update_cart_usecase, cart_repository, cart_item_repository, product_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,10)
    
    product_price = 50.0
    product = Product(id=product_id, name="Test Product", price=product_price, category=ProductCategory.BURGER)
    
    cart = Cart(id=cart_id, user_id=user_id, total_price=0.0)
    
    # Criar um item de carrinho para evitar o erro "Cart items not found for this cart"
    cart_item = CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=1)
    
    cart_repository.find_cart = async_return(cart)
    product_repository.find_product = async_return(product)
    cart_item_repository.find_items_by_cart_id = async_return([cart_item])
    cart_repository.update_cart = async_return(Cart(id=cart_id, user_id=user_id, total_price=product_price))
    cart_item_repository.update_item = async_return(cart_item)
    
    input_dto = UpdateCartInputDto(items=[UpdateCartItemDto(product_id=product_id, quantity=1)])
    
    # Substituindo run_async por await
    output_dto = await update_cart_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    
    assert output_dto.id == cart_id
    assert output_dto.user_id == user_id
    assert output_dto.total_price == product_price
    
    assert cart_repository.find_cart.called
    assert cart_item_repository.find_items_by_cart_id.called
    assert cart_repository.update_cart.called

@pytest.mark.asyncio
async def test_update_cart_cart_not_found(update_cart_usecase, cart_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,10)
    cart_repository.find_cart = async_return(None)
    input_dto = UpdateCartInputDto(items=[UpdateCartItemDto(product_id=product_id, quantity=1)])
    
    with pytest.raises(ValueError) as excinfo:
        # Substituindo run_async por await
        await update_cart_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    
    assert str(excinfo.value) == f"Cart not found"
    cart_repository.find_cart.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_cart_items_not_found(update_cart_usecase, cart_repository, cart_item_repository):
    user_id = uuid4()
    cart_id = uuid4()
    product_id = random.randint(1,10)
    cart = Cart(id=cart_id, user_id=user_id, total_price=0.0)
    cart_repository.find_cart = async_return(cart)
    cart_item_repository.find_items_by_cart_id = async_return([])
    input_dto = UpdateCartInputDto(items=[UpdateCartItemDto(product_id=product_id, quantity=1)])
    
    with pytest.raises(ValueError) as excinfo:
        # Substituindo run_async por await
        await update_cart_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    
    assert str(excinfo.value) == f"Cart items not found for this cart"
    cart_repository.find_cart.assert_awaited_once()
    cart_item_repository.find_items_by_cart_id.assert_awaited_once()