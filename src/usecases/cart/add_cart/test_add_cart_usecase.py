import random
import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.cart.cart_entity import Cart
from domain.cart_item.cart_item_entity import CartItem
from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.cart.add_cart.add_cart_dto import AddCartInputDto, CartItemDto
from usecases.cart.add_cart.add_cart_usecase import AddCartUseCase


@pytest.fixture
def cart_repository():
    repo = Mock()
    repo.add_cart = AsyncMock()
    return repo

@pytest.fixture
def cart_item_repository():
    repo = Mock()
    repo.add_item = AsyncMock()
    return repo

@pytest.fixture
def user_repository():
    repo = Mock()
    repo.find_user = AsyncMock()
    return repo

@pytest.fixture
def product_repository():
    repo = Mock()
    repo.find_product = AsyncMock()
    return repo

@pytest.fixture
def add_cart_usecase(cart_repository, cart_item_repository, user_repository, product_repository):
    return AddCartUseCase(cart_repository, cart_item_repository, user_repository, product_repository)

@pytest.mark.asyncio
async def test_add_cart_success(add_cart_usecase, cart_repository, cart_item_repository, user_repository, product_repository):
    user_id = uuid.uuid4()
    product_id = random.randint(1, 100)
    age = 25
    gender = UserGender.MALE
    user = User(id=user_id, name="Test User", email="test@example.com", age=age, gender=gender, phone_number="1234567890", password="password")
    product = Product(id=product_id, name="Test Product", price=100.0, category=ProductCategory.SIDE_DISH)
    
    user_repository.find_user = async_return(user)
    product_repository.find_product = async_return(product)
    
    input_dto = AddCartInputDto(items=[CartItemDto(product_id=product_id, quantity=2)])
    
    output_dto = await add_cart_usecase.execute(user_id=user_id, input=input_dto)
    
    assert output_dto.user_id == user_id
    assert output_dto.total_price == 200.0
    assert cart_repository.add_cart.await_count == 1
    assert cart_item_repository.add_item.await_count == 1

@pytest.mark.asyncio
async def test_add_cart_user_not_found(add_cart_usecase, user_repository):
    user_id = uuid.uuid4()
    user_repository.find_user = async_return(None)
    
    input_dto = AddCartInputDto(items=[])
    
    with pytest.raises(ValueError) as excinfo:
        await add_cart_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"User with id '{user_id}' not found"

@pytest.mark.asyncio
async def test_add_cart_product_not_found(add_cart_usecase, user_repository, product_repository):
    user_id = uuid.uuid4()
    product_id = random.randint(1, 100)
    age = 25
    gender = UserGender.MALE
    user = User(id=user_id, name="Test User", email="test@example.com", age=age, gender=gender, phone_number="1234567890", password="password")
    
    user_repository.find_user = async_return(user)
    product_repository.find_product = async_return(None)
    
    input_dto = AddCartInputDto(items=[CartItemDto(product_id=product_id, quantity=2)])
    
    with pytest.raises(ValueError) as excinfo:
        await add_cart_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Product with code '{product_id}' not found"