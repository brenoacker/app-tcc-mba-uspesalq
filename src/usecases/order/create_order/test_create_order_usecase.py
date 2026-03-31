import random
from datetime import datetime, timedelta
from decimal import Decimal  # Added
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

# from domain.__seedwork.test_utils import (async_return, async_side_effect, run_async) # run_async not used
from domain.cart.cart_entity import Cart
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from domain.payment.payment_entity import Payment # Added for type hinting if needed
from domain.payment.payment_status_enum import PaymentStatus # Added for type hinting
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.order.create_order.create_order_dto import CreateOrderInputDto
from usecases.order.create_order.create_order_usecase import CreateOrderUseCase

# Helper for async return value for mocks
def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f

@pytest.fixture
def order_repository():
    repo = Mock(spec=OrderRepositoryInterface) # Use spec for better mocking
    repo.create_order = AsyncMock()
    repo.find_order_by_cart_id = AsyncMock()
    return repo

@pytest.fixture
def user_repository():
    repo = Mock(spec=UserRepositoryInterface)
    repo.find_user = AsyncMock()
    return repo

@pytest.fixture
def cart_repository():
    repo = Mock(spec=CartRepositoryInterface)
    repo.find_cart = AsyncMock()
    return repo

@pytest.fixture
def offer_repository():
    repo = Mock(spec=OfferRepositoryInterface)
    repo.find_offer = AsyncMock()
    return repo

@pytest.fixture
def payment_repository():
    repo = Mock(spec=PaymentRepositoryInterface)
    repo.create_payment = AsyncMock()
    return repo

@pytest.fixture
def create_order_usecase(order_repository, user_repository, cart_repository, offer_repository, payment_repository):
    return CreateOrderUseCase(order_repository, user_repository, cart_repository, offer_repository, payment_repository)

@pytest.mark.asyncio
async def test_create_order_success(create_order_usecase, order_repository, user_repository, cart_repository, offer_repository, payment_repository):
    user_id = uuid4()
    cart_id = uuid4()
    offer_id = random.randint(1,100)
    order_type = OrderType.DELIVERY
    
    mock_user = User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.FEMALE, phone_number="1234567890", password="testpassword")
    user_repository.find_user.return_value = mock_user # Use direct return_value for async_return pattern if it's simpler

    # Cart total price is Decimal
    mock_cart = Cart(id=cart_id, user_id=user_id, total_price=Decimal('100.00'))
    cart_repository.find_cart.return_value = mock_cart

    # Offer discount value is Decimal
    mock_offer = Offer(id=offer_id, discount_type=OfferType.PERCENTAGE, discount_value=Decimal('10.0'), start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10))
    offer_repository.find_offer.return_value = mock_offer
    
    order_repository.find_order_by_cart_id.return_value = None
    
    # Expected total price after 10% discount on 100.00 is 90.00
    expected_final_price = Decimal('90.00')
    
    # Mock the created order
    order_id_generated = uuid4() # Capture the generated order ID for payment check
    mock_created_order = Order(id=order_id_generated, user_id=user_id, cart_id=cart_id, type=order_type, total_price=expected_final_price, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=offer_id)
    order_repository.create_order.return_value = mock_created_order
    
    # Mock payment creation
    mock_payment = Payment(id=uuid4(), user_id=user_id, order_id=order_id_generated, payment_method=None, payment_card_gateway=None, status=PaymentStatus.PENDING)
    payment_repository.create_payment.return_value = mock_payment
    
    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=offer_id, type=order_type)
    
    output_dto = await create_order_usecase.execute(user_id=user_id, input=input_dto)
    
    assert output_dto.total_price == expected_final_price # Compare Decimals
    assert output_dto.type == order_type
    assert output_dto.status == OrderStatus.PENDING
    
    user_repository.find_user.assert_awaited_once_with(user_id=user_id)
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)
    offer_repository.find_offer.assert_awaited_once_with(offer_id=offer_id)
    order_repository.find_order_by_cart_id.assert_awaited_once_with(cart_id=cart_id)
    
    # Check that create_order was called with an Order instance where total_price is Decimal
    called_order_arg = order_repository.create_order.call_args[1]['order'] # Using kwargs access
    assert isinstance(called_order_arg.total_price, Decimal)
    assert called_order_arg.total_price == expected_final_price
    
    payment_repository.create_payment.assert_awaited_once()
    called_payment_arg = payment_repository.create_payment.call_args[1]['payment']
    assert called_payment_arg.order_id == order_id_generated


@pytest.mark.asyncio
async def test_create_order_user_not_found(create_order_usecase, user_repository):
    user_id = uuid4()
    cart_id = uuid4()
    user_repository.find_user.return_value = None
    
    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=None, type=OrderType.DELIVERY)
    
    with pytest.raises(ValueError) as excinfo:
        await create_order_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"User with id '{user_id}' not found"
    user_repository.find_user.assert_awaited_once_with(user_id=user_id)

@pytest.mark.asyncio
async def test_create_order_cart_not_found(create_order_usecase, user_repository, cart_repository):
    user_id = uuid4()
    cart_id = uuid4()
    mock_user = User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.FEMALE, phone_number="1234567890", password="testpassword")
    user_repository.find_user.return_value = mock_user
    cart_repository.find_cart.return_value = None
    
    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=None, type=OrderType.DELIVERY)
    
    with pytest.raises(ValueError) as excinfo:
        await create_order_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Cart with id '{cart_id}' not found"
    user_repository.find_user.assert_awaited_once_with(user_id=user_id)
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)

@pytest.mark.asyncio
async def test_create_order_offer_not_found(create_order_usecase, user_repository, cart_repository, offer_repository):
    user_id = uuid4()
    cart_id = uuid4()
    offer_id = random.randint(1,100)
    mock_user = User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.FEMALE, phone_number="1234567890", password="testpassword")
    user_repository.find_user.return_value = mock_user
    # Cart total price is Decimal
    mock_cart = Cart(id=cart_id, user_id=user_id, total_price=Decimal('100.00'))
    cart_repository.find_cart.return_value = mock_cart
    offer_repository.find_offer.return_value = None
    
    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=offer_id, type=OrderType.DELIVERY)
    
    with pytest.raises(ValueError) as excinfo:
        await create_order_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Offer with id '{offer_id}' not found"
    user_repository.find_user.assert_awaited_once_with(user_id=user_id)
    cart_repository.find_cart.assert_awaited_once_with(cart_id=cart_id, user_id=user_id)
    offer_repository.find_offer.assert_awaited_once_with(offer_id=offer_id)

@pytest.mark.asyncio
async def test_create_order_order_already_exists(create_order_usecase, user_repository, cart_repository, order_repository):
    user_id = uuid4()
    cart_id = uuid4()
    mock_user = User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.FEMALE, phone_number="1234567890", password="testpassword")
    user_repository.find_user.return_value = mock_user
    # Order total price is Decimal
    mock_existing_order = Order(id=uuid4(), user_id=user_id, cart_id=cart_id, total_price=Decimal('100.00'), type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=None)
    order_repository.find_order_by_cart_id.return_value = mock_existing_order

    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=None, type=OrderType.DELIVERY)

    with pytest.raises(ValueError) as excinfo:
        await create_order_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Order for cart_id '{cart_id}' already exists"
    user_repository.find_user.assert_called_once_with(user_id=user_id) # find_user is not awaited in this path
    order_repository.find_order_by_cart_id.assert_awaited_once_with(cart_id=cart_id)


@pytest.mark.asyncio
async def test_create_order_failed_to_create_order(create_order_usecase, user_repository, cart_repository, offer_repository, order_repository):
    user_id = uuid4()
    cart_id = uuid4()
    offer_id = random.randint(1,100)
    mock_user = User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    user_repository.find_user.return_value = mock_user
    mock_cart = Cart(id=cart_id, user_id=user_id, total_price=Decimal('100.00'))
    cart_repository.find_cart.return_value = mock_cart
    mock_offer = Offer(id=offer_id, discount_type=OfferType.PERCENTAGE, discount_value=Decimal('10.0'), start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10))
    offer_repository.find_offer.return_value = mock_offer
    order_repository.find_order_by_cart_id.return_value = None
    order_repository.create_order.return_value = None # Simulate failure

    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=offer_id, type=OrderType.DELIVERY)

    with pytest.raises(ValueError) as excinfo:
        await create_order_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Failed to create order for cart with id '{cart_id}'"
    # order_repository.create_order.assert_awaited_once() # This was missing await_count in original

@pytest.mark.asyncio
async def test_create_order_order_created_but_not_pending(create_order_usecase, user_repository, cart_repository, offer_repository, order_repository):
    user_id = uuid4()
    cart_id = uuid4()
    offer_id = random.randint(1,100)
    mock_user = User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    user_repository.find_user.return_value = mock_user
    mock_cart = Cart(id=cart_id, user_id=user_id, total_price=Decimal('100.00'))
    cart_repository.find_cart.return_value = mock_cart
    mock_offer = Offer(id=offer_id, discount_type=OfferType.PERCENTAGE, discount_value=Decimal('10.0'), start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10))
    offer_repository.find_offer.return_value = mock_offer
    order_repository.find_order_by_cart_id.return_value = None
    # Order created with status CONFIRMED instead of PENDING
    mock_created_order_wrong_status = Order(id=uuid4(), user_id=user_id, cart_id=cart_id, total_price=Decimal('90.00'), type=OrderType.DELIVERY, status=OrderStatus.CONFIRMED, created_at=datetime.now(), updated_at=datetime.now(), offer_id=offer_id)
    order_repository.create_order.return_value = mock_created_order_wrong_status

    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=offer_id, type=OrderType.DELIVERY)

    with pytest.raises(ValueError) as excinfo:
        await create_order_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Order was created but with '{OrderStatus.CONFIRMED}' status, not 'PENDING'"


@pytest.mark.asyncio
async def test_create_order_failed_to_create_payment(create_order_usecase, user_repository, cart_repository, offer_repository, order_repository, payment_repository):
    user_id = uuid4()
    cart_id = uuid4()
    offer_id = random.randint(1,100)
    order_id_generated = uuid4()
    mock_user = User(id=user_id, name="Test User", email="test@example.com", age=25, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    user_repository.find_user.return_value = mock_user
    mock_cart = Cart(id=cart_id, user_id=user_id, total_price=Decimal('100.00'))
    cart_repository.find_cart.return_value = mock_cart
    mock_offer = Offer(id=offer_id, discount_type=OfferType.PERCENTAGE, discount_value=Decimal('10.0'), start_date=datetime.now(), end_date=datetime.now() + timedelta(days=10))
    offer_repository.find_offer.return_value = mock_offer
    order_repository.find_order_by_cart_id.return_value = None
    mock_created_order = Order(id=order_id_generated, user_id=user_id, cart_id=cart_id, total_price=Decimal('90.00'), type=OrderType.DELIVERY, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=offer_id)
    order_repository.create_order.return_value = mock_created_order
    
    payment_repository.create_payment.return_value = None # Simulate failure

    input_dto = CreateOrderInputDto(cart_id=cart_id, offer_id=offer_id, type=OrderType.DELIVERY)

    with pytest.raises(ValueError) as excinfo:
        await create_order_usecase.execute(user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Failed to create payment for order with id '{order_id_generated}'"

# Need to import asyncio for the async_return helper if it's defined in this file
import asyncio

# Add definition of OrderRepositoryInterface, UserRepositoryInterface, etc. if not globally available
# For this test file, they are imported from the domain, so that's fine.
# However, the Mock(spec=...) requires these to be actual classes/ABCs.
# Let's assume they are correctly imported and spec works.
# If not, we might need to define dummy interfaces or remove spec for simplicity if tool struggles.
from domain.order.order_repository_interface import OrderRepositoryInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from domain.cart.cart_repository_interface import CartRepositoryInterface
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from domain.payment.payment_repository_interface import PaymentRepositoryInterface
