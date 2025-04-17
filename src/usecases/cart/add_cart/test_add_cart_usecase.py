import random
import uuid
from unittest.mock import Mock

import pytest

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.cart.add_cart.add_cart_dto import AddCartInputDto, CartItemDto
from usecases.cart.add_cart.add_cart_usecase import AddCartUseCase


@pytest.fixture
def cart_repository():
    return Mock()

@pytest.fixture
def cart_item_repository():
    return Mock()

@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def product_repository():
    return Mock()

@pytest.fixture
def add_cart_usecase(cart_repository, cart_item_repository, user_repository, product_repository):
    return AddCartUseCase(cart_repository, cart_item_repository, user_repository, product_repository)

def test_add_cart_success(add_cart_usecase, cart_repository, cart_item_repository, user_repository, product_repository):
    user_id = uuid.uuid4()
    product_id = random.randint(1, 100)
    age = 25
    gender = UserGender.MALE
    user_repository.find_user.return_value = User(id=user_id, name="Test User", email="test@example.com", age=age, gender=gender, phone_number="1234567890", password="password")
    product_repository.find_product.return_value = Product(id=product_id, name="Test Product", price=100.0, category=ProductCategory.SIDE_DISH)
    
    input_dto = AddCartInputDto(items=[CartItemDto(product_id=product_id, quantity=2)])
    
    output_dto = add_cart_usecase.execute(user_id=user_id, input=input_dto)
    
    assert output_dto.user_id == user_id
    assert output_dto.total_price == 200.0
    cart_repository.add_cart.assert_called_once()
    cart_item_repository.add_item.assert_called_once()

def test_add_cart_user_not_found(add_cart_usecase, user_repository):
    user_id = uuid.uuid4()
    user_repository.find_user.return_value = None
    
    input_dto = AddCartInputDto(items=[])
    
    with pytest.raises(ValueError) as excinfo:
        add_cart_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"User with id '{user_id}' not found"

def test_add_cart_product_not_found(add_cart_usecase, user_repository, product_repository):
    user_id = uuid.uuid4()
    product_id = random.randint(1, 100)
    age = 25
    gender = UserGender.MALE
    user_repository.find_user.return_value = User(id=user_id, name="Test User", email="test@example.com", age=age, gender=gender, phone_number="1234567890", password="password")
    product_repository.find_product.return_value = None
    
    input_dto = AddCartInputDto(items=[CartItemDto(product_id=product_id, quantity=2)])
    
    with pytest.raises(ValueError) as excinfo:
        add_cart_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Product with code '{product_id}' not found"