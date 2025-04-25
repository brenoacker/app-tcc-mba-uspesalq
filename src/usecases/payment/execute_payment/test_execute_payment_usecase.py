import asyncio
import random
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
from usecases.payment.execute_payment.execute_payment_dto import \
    ExecutePaymentInputDto
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
    
    # Configuração dos mocks
    user = User(id=user_id, name="Test User", email="test@example.com", age=33, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now())
    payment = Payment(id=payment_id, user_id=user_id, order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO, status=PaymentStatus.PENDING)
    
    user_repository.find_user = async_return(user)
    order_repository.find_order = async_return(order)
    payment_repository.find_payment_by_order_id = async_return(payment)
    
    # Mock para objetos retornados após atualizações
    updated_payment = Payment(id=payment_id, user_id=user_id, order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO, status=PaymentStatus.PAID)
    updated_order = Order(id=order_id, user_id=user_id, cart_id=order.cart_id, total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.CONFIRMED, created_at=order.created_at, updated_at=datetime.now())
    
    payment_repository.execute_payment = async_return(updated_payment)
    order_repository.update_order = async_return(updated_order)

    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)

    # Não precisamos mais patchar asyncio.sleep, pois removemos do código de produção
    output_dto = await execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)

    # Verificações
    assert output_dto.id == payment_id
    assert output_dto.order_id == order_id
    assert output_dto.user_id == user_id
    assert output_dto.payment_method == PaymentMethod.CARD
    assert output_dto.status == PaymentStatus.PAID
    
    # Verificar que as consultas assíncronas foram chamadas
    user_repository.find_user.assert_awaited_once()
    order_repository.find_order.assert_awaited_once()
    payment_repository.find_payment_by_order_id.assert_awaited_once()
    
    # Verificar que as operações de atualização foram chamadas
    payment_repository.execute_payment.assert_awaited_once()
    order_repository.update_order.assert_awaited_once()
    
    # Verificamos apenas que ambas foram chamadas (não é possível verificar a ordem 
    # exata porque estamos usando gather() para execução paralela)
    assert payment_repository.execute_payment.call_count == 1
    assert order_repository.update_order.call_count == 1

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
    cart_id = uuid4()
    order_id = uuid4()
    
    # Configuração para order já confirmado
    user = User(id=user_id, name="Test User", email="test@example.com", age=33, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    order = Order(id=order_id, user_id=user_id, cart_id=cart_id, total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.CONFIRMED, created_at=datetime.now(), updated_at=datetime.now(), offer_id=None)
    
    user_repository.find_user = async_return(user)
    order_repository.find_order = async_return(order)
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)
    
    with pytest.raises(ValueError) as excinfo:
        await execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)
    assert f"Order with id {order_id} already confirmed" in str(excinfo.value)
    user_repository.find_user.assert_awaited_once_with(user_id)
    order_repository.find_order.assert_awaited_once_with(order_id=order_id, user_id=user_id)

@pytest.mark.asyncio
async def test_execute_payment_payment_not_found(execute_payment_usecase, user_repository, order_repository, payment_repository):
    user_id = uuid4()
    order_id = uuid4()
    
    # Configuração dos mocks
    user = User(id=user_id, name="Test User", email="test@example.com", age=18, gender=UserGender.FEMALE, phone_number="1234567890", password="testpassword")
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), type=OrderType.DRIVE_THRU, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), total_price=100.0)
    
    user_repository.find_user = async_return(user)
    order_repository.find_order = async_return(order)
    payment_repository.find_payment_by_order_id = async_return(None)
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)

    with pytest.raises(ValueError) as excinfo:
        await execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)

    assert str(excinfo.value) == f"Payment for order with id {order_id} not found"

@pytest.mark.asyncio
async def test_execute_payment_payment_already_paid(execute_payment_usecase, user_repository, order_repository, payment_repository):
    user_id = uuid4()
    order_id = uuid4()
    
    # Configuração dos mocks
    user = User(id=user_id, name="Test User", email="test@example.com", age=18, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), type=OrderType.DRIVE_THRU, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), total_price=100.0)
    payment = Payment(id=uuid4(), user_id=user_id, order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO, status=PaymentStatus.PAID)
    
    user_repository.find_user = async_return(user)
    order_repository.find_order = async_return(order)
    payment_repository.find_payment_by_order_id = async_return(payment)
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)

    with pytest.raises(ValueError) as excinfo:
        await execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)

    assert str(excinfo.value) == f"Payment for order with id {order_id} already paid"

@pytest.mark.asyncio
async def test_execute_payment_with_offer(execute_payment_usecase, user_repository, order_repository, payment_repository):
    # Configuração dos dados de teste
    user_id = uuid4()
    order_id = uuid4()
    payment_id = uuid4()
    
    # Configuração dos objetos
    user = User(id=user_id, name="Test User", email="test@example.com", age=18, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    order = Order(id=order_id, user_id=user_id, cart_id=uuid4(), type=OrderType.DRIVE_THRU, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), total_price=100.0, offer_id=random.randint(1,100))
    payment = Payment(id=payment_id, user_id=user_id, order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO, status=PaymentStatus.PENDING)
    
    # Configuração dos mocks
    user_repository.find_user = async_return(user)
    order_repository.find_order = async_return(order)
    payment_repository.find_payment_by_order_id = async_return(payment)
    
    # Objetos atualizados após operações
    updated_order = Order(
        id=order_id, 
        user_id=user_id, 
        cart_id=order.cart_id, 
        type=order.type, 
        status=OrderStatus.CONFIRMED, 
        created_at=order.created_at, 
        updated_at=datetime.now(), 
        total_price=order.total_price,
        offer_id=order.offer_id
    )
    
    updated_payment = Payment(
        id=payment_id, 
        user_id=user_id, 
        order_id=order_id, 
        payment_method=PaymentMethod.CARD, 
        payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO, 
        status=PaymentStatus.PAID
    )
    
    order_repository.update_order = async_return(updated_order)
    payment_repository.execute_payment = async_return(updated_payment)
    
    input_dto = ExecutePaymentInputDto(
        payment_method=PaymentMethod.CARD, 
        payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO
    )

    # Executar o caso de uso (não precisamos mais patchar asyncio.sleep)
    output_dto = await execute_payment_usecase.execute(
        order_id=order_id, 
        user_id=user_id, 
        input=input_dto
    )
    
    # Verificações
    assert output_dto.status == PaymentStatus.PAID
    assert output_dto.payment_method == PaymentMethod.CARD
    assert output_dto.payment_card_gateway == PaymentCardGateway.PAYPAL_VENMO
    
    # Verificamos que ambas as operações foram chamadas
    payment_repository.execute_payment.assert_awaited_once()
    order_repository.update_order.assert_awaited_once()
    
    # Verificar que as atualizações foram feitas com os valores corretos
    assert order_repository.update_order.call_args[1]['order'].status == OrderStatus.CONFIRMED
    assert payment_repository.execute_payment.call_args[1]['payment'].status == PaymentStatus.PAID
