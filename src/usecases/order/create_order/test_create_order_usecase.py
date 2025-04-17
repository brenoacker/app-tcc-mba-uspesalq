import random
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from domain.cart.cart_entity import Cart
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.order.create_order.create_order_dto import (CreateOrderInputDto,
                                                          CreateOrderOutputDto)
from usecases.order.create_order.create_order_usecase import CreateOrderUseCase


@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def cart_repository():
    return Mock()

@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def create_order_usecase(order_repository, user_repository, cart_repository, offer_repository):
    return CreateOrderUseCase(order_repository, user_repository, cart_repository, offer_repository)

@pytest.mark.asyncio
async def test_create_order_success(create_order_usecase, order_repository, user_repository, cart_repository, offer_repository):
    user_id = uuid4()
    cart_id = uuid4()
    offer_id = random.randint(1,100)
    order_type = OrderType.DELIVERY
    user_repository.find_user = async_return(User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.FEMALE, phone_number="1234567890", password="testpassword"))
    cart_repository.find_cart = async_return(Cart(id=cart_id, user_id=user_id, total_price=100.0))
    offer_repository.find_offer = async_return(Offer(id=offer_id, discount_type=OfferType.PERCENTAGE, discount_value=10.0, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10)))
    order_repository.find_order_by_cart_id = async_return(None)
    order_repository.create_order = async_return(Order(id=uuid4(), user_id=user_id, cart_id=cart_id, type=order_type, total_price=90.0, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=offer_id))
    
    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=offer_id, type=order_type)
    
    output_dto = await create_order_usecase.execute(user_id=user_id, input=input_dto)
    
    assert output_dto.total_price == 90.0
    assert output_dto.type == order_type
    assert output_dto.status == OrderStatus.PENDING
    user_repository.find_user.assert_awaited_once_with()
    cart_repository.find_cart.assert_awaited_once_with()
    offer_repository.find_offer.assert_awaited_once_with()
    order_repository.create_order.await_count == 1

@pytest.mark.asyncio
async def test_create_order_user_not_found(create_order_usecase, user_repository):
    user_id = uuid4()
    cart_id = uuid4()
    user_repository.find_user = async_return(None)
    
    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=None, type=OrderType.DELIVERY)
    
    with pytest.raises(ValueError) as excinfo:
        run_async(create_order_usecase.execute(user_id=user_id, input=input_dto))
    assert str(excinfo.value) == f"User with id '{user_id}' not found"
    user_repository.find_user.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_create_order_cart_not_found(create_order_usecase, user_repository, cart_repository):
    user_id = uuid4()
    cart_id = uuid4()
    user_repository.find_user = async_return(User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.FEMALE, phone_number="1234567890", password="testpassword"))
    cart_repository.find_cart = async_return(None)
    
    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=None, type=OrderType.DELIVERY)
    
    with pytest.raises(ValueError) as excinfo:
        run_async(create_order_usecase.execute(user_id=user_id, input=input_dto))
    assert str(excinfo.value) == f"Cart with id '{cart_id}' not found"
    user_repository.find_user.assert_awaited_once_with()
    cart_repository.find_cart.assert_awaited_once_with()

@pytest.mark.asyncio
async def test_create_order_offer_not_found(create_order_usecase, user_repository, cart_repository, offer_repository):
    user_id = uuid4()
    cart_id = uuid4()
    offer_id = random.randint(1,100)
    user_repository.find_user = async_return(User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.FEMALE, phone_number="1234567890", password="testpassword"))
    cart_repository.find_cart = async_return(Cart(id=cart_id, user_id=user_id, total_price=100.0))
    offer_repository.find_offer = async_return(None)
    
    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=offer_id, type=OrderType.DELIVERY)
    
    with pytest.raises(ValueError) as excinfo:
        run_async(create_order_usecase.execute(user_id=user_id, input=input_dto))
    assert str(excinfo.value) == f"Offer with id '{offer_id}' not found"
    user_repository.find_user.assert_awaited_once_with()
    cart_repository.find_cart.assert_awaited_once_with()
    offer_repository.find_offer.assert_awaited_once_with()