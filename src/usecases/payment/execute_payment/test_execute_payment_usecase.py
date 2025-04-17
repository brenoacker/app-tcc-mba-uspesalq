from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.payment.execute_payment.execute_payment_dto import (
    ExecutePaymentInputDto, ExecutePaymentOutputDto)
from usecases.payment.execute_payment.execute_payment_usecase import \
    ExecutePaymentUseCase


@pytest.fixture
def payment_repository():
    repo = Mock()
    repo.find_payment_by_order_id = AsyncMock()
    repo.execute_payment = AsyncMock()
    return repo

@pytest.fixture
def user_repository():
    repo = Mock()
    repo.find_user = AsyncMock()
    return repo

@pytest.fixture
def order_repository():
    repo = Mock()
    repo.find_order = AsyncMock()
    repo.update_order = AsyncMock()
    return repo

@pytest.fixture
def execute_payment_usecase(payment_repository, user_repository, order_repository):
    return ExecutePaymentUseCase(payment_repository, user_repository, order_repository)

@pytest.mark.asyncio
async def test_execute_payment_success(execute_payment_usecase, payment_repository, user_repository, order_repository):
    user_id = uuid4()
    order_id = uuid4()
    payment_id = uuid4()
    user_repository.find_user = async_return(User(id=user_id, name="Test User", email="test@example.com", age=33, gender=UserGender.MALE, phone_number="1234567890", password="testpassword"))
    order_repository.find_order = async_return(Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now()))
    payment_repository.find_payment_by_order_id = async_return(Payment(id=payment_id, user_id=user_id, order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO, status=PaymentStatus.PENDING))
    payment_repository.execute_payment = async_return(Payment(id=payment_id, user_id=user_id, order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO, status=PaymentStatus.PAID))
    order_repository.update_order = async_return(Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.CONFIRMED, created_at=datetime.now(), updated_at=datetime.now()))

    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)

    output_dto = await execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)

    assert output_dto.id == payment_id
    assert output_dto.order_id == order_id
    assert output_dto.user_id == user_id
    assert output_dto.payment_method == PaymentMethod.CARD
    assert output_dto.status == PaymentStatus.PAID

@pytest.mark.asyncio
async def test_execute_payment_user_not_found(execute_payment_usecase, user_repository):
    user_id = uuid4()
    order_id = uuid4()
    user_repository.find_user = async_return(None)

    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)

    with pytest.raises(ValueError) as excinfo:
        await execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"User with id {user_id} not found"
    user_repository.find_user.assert_awaited_once_with(user_id)

@pytest.mark.asyncio
async def test_execute_payment_order_not_found(execute_payment_usecase, user_repository, order_repository):
    user_id = uuid4()
    order_id = uuid4()
    user_repository.find_user = async_return(User(id=user_id, name="Test User", email="test@example.com", age=33, gender=UserGender.MALE, phone_number="1234567890", password="testpassword"))
    order_repository.find_order = async_return(None)
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)
    
    with pytest.raises(ValueError) as excinfo:
        await execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Order with id {order_id} not found"
    user_repository.find_user.assert_awaited_once_with(user_id)
    order_repository.find_order.assert_awaited_once_with(order_id=order_id, user_id=user_id)

@pytest.mark.asyncio
async def test_execute_payment_order_already_confirmed(execute_payment_usecase, user_repository, order_repository):
    user_id = uuid4()
    order_id = uuid4()
    cart_id = uuid4()
    user_repository.find_user = async_return(User(id=user_id, name="Test User", email="test@example.com", age=33, gender=UserGender.MALE, phone_number="1234567890", password="testpassword"))
    order_repository.find_order = async_return(Order(id=order_id, user_id=user_id, cart_id=cart_id, total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.CONFIRMED, created_at=datetime.now(), updated_at=datetime.now(), offer_id=None))
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)
    
    with pytest.raises(ValueError) as excinfo:
        await execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)
    assert f"Order with id {order_id} already confirmed" in str(excinfo.value)
    user_repository.find_user.assert_awaited_once_with(user_id)
    order_repository.find_order.assert_awaited_once_with(order_id=order_id, user_id=user_id)