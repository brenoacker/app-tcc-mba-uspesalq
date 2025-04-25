from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.payment.find_payment_by_order_id.find_payment_by_order_id_dto import \
    FindPaymentByOrderIdInputDto
from usecases.payment.find_payment_by_order_id.find_payment_by_order_id_usecase import \
    FindPaymentByOrderIdUsecase


@pytest.fixture
def payment_repository():
    repo = Mock()
    repo.find_payment_by_order_id = AsyncMock()
    return repo

@pytest.fixture
def user_repository():
    repo = Mock()
    repo.find_user = AsyncMock()
    return repo

@pytest.fixture
def find_payment_by_order_id_usecase(payment_repository, user_repository):
    return FindPaymentByOrderIdUsecase(payment_repository, user_repository)

@pytest.mark.asyncio
async def test_find_payment_by_order_id_success(find_payment_by_order_id_usecase, payment_repository, user_repository):
    user_id = uuid4()
    order_id = uuid4()
    payment_id = uuid4()
    
    # Criar um usuário de teste
    user = User(id=user_id, name="Test User", email="test@example.com", age=30, gender=UserGender.MALE, phone_number="1234567890", password="password")
    user_repository.find_user = async_return(user)
    
    # Criar um pagamento de teste
    payment = Payment(id=payment_id, user_id=user_id, order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.ADYEN, status=PaymentStatus.PAID)
    payment_repository.find_payment_by_order_id = async_return(payment)
    
    input_dto = FindPaymentByOrderIdInputDto(order_id=order_id, user_id=user_id)
    
    output_dto = await find_payment_by_order_id_usecase.execute(input=input_dto)
    
    assert output_dto.id == payment_id
    assert output_dto.user_id == user_id
    assert output_dto.order_id == order_id
    assert output_dto.payment_method == PaymentMethod.CARD
    assert output_dto.payment_card_gateway == PaymentCardGateway.ADYEN
    assert output_dto.status == PaymentStatus.PAID
    
    user_repository.find_user.assert_awaited_once_with(user_id=user_id)
    payment_repository.find_payment_by_order_id.assert_awaited_once_with(order_id=order_id)

@pytest.mark.asyncio
async def test_find_payment_by_order_id_user_not_found(find_payment_by_order_id_usecase, user_repository):
    user_id = uuid4()
    order_id = uuid4()
    
    # Configurar o mock para retornar None, simulando que o usuário não foi encontrado
    user_repository.find_user = async_return(None)
    
    input_dto = FindPaymentByOrderIdInputDto(order_id=order_id, user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        await find_payment_by_order_id_usecase.execute(input=input_dto)
    
    assert str(excinfo.value) == f"User with id {user_id} not found"
    user_repository.find_user.assert_awaited_once_with(user_id=user_id)

@pytest.mark.asyncio
async def test_find_payment_by_order_id_payment_not_found(find_payment_by_order_id_usecase, user_repository, payment_repository):
    user_id = uuid4()
    order_id = uuid4()
    
    # Criar um usuário de teste
    user = User(id=user_id, name="Test User", email="test@example.com", age=30, gender=UserGender.MALE, phone_number="1234567890", password="password")
    user_repository.find_user = async_return(user)
    
    # Configurar o mock para retornar None, simulando que o pagamento não foi encontrado
    payment_repository.find_payment_by_order_id = async_return(None)
    
    input_dto = FindPaymentByOrderIdInputDto(order_id=order_id, user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        await find_payment_by_order_id_usecase.execute(input=input_dto)
    
    assert str(excinfo.value) == f"Payment for order with id {order_id} not found"
    user_repository.find_user.assert_awaited_once_with(user_id=user_id)
    payment_repository.find_payment_by_order_id.assert_awaited_once_with(order_id=order_id)