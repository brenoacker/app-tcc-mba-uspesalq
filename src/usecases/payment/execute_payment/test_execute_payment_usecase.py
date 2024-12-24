from datetime import datetime
from unittest.mock import Mock, patch
from uuid import uuid4

import pytest

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
    return Mock()

@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def execute_payment_usecase(payment_repository, user_repository, order_repository):
    return ExecutePaymentUseCase(payment_repository, user_repository, order_repository)

def test_execute_payment_success(execute_payment_usecase, payment_repository, user_repository, order_repository):
    user_id = uuid4()
    order_id = uuid4()
    user_repository.find_user.return_value = User(id=user_id, name="Test User", email="test@example.com", age=33, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    order_repository.find_order.return_value = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=None)
    payment_repository.execute_payment.return_value = Payment(id=uuid4(), user_id=user_id, order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.ADYEN, status=PaymentStatus.PAID)
    order_repository.update_order.return_value = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.CONFIRMED, created_at=datetime.now(), updated_at=datetime.now(), offer_id=None)
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.ADYEN)
    
    with patch("time.sleep", return_value=None):
        output_dto = execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)
    
    assert output_dto.status == PaymentStatus.PAID
    assert output_dto.payment_method == PaymentMethod.CARD
    assert output_dto.payment_card_gateway == PaymentCardGateway.ADYEN
    user_repository.find_user.assert_called_once_with(user_id)
    order_repository.find_order.assert_called_once_with(order_id)
    payment_repository.execute_payment.assert_called_once()
    order_repository.update_order.assert_called_once()

def test_execute_payment_user_not_found(execute_payment_usecase, user_repository):
    user_id = uuid4()
    order_id = uuid4()
    user_repository.find_user.return_value = None
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)
    
    with pytest.raises(ValueError) as excinfo:
        execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"User with id {user_id} not found"
    user_repository.find_user.assert_called_once_with(user_id)

def test_execute_payment_order_not_found(execute_payment_usecase, user_repository, order_repository):
    user_id = uuid4()
    order_id = uuid4()
    user_repository.find_user.return_value =User(id=user_id, name="Test User", email="test@example.com", age=33, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    order_repository.find_order.return_value = None
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)
    
    with pytest.raises(ValueError) as excinfo:
        execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Order with id {order_id} not found"
    user_repository.find_user.assert_called_once_with(user_id)
    order_repository.find_order.assert_called_once_with(order_id)

def test_execute_payment_order_already_confirmed(execute_payment_usecase, user_repository, order_repository):
    user_id = uuid4()
    order_id = uuid4()
    user_repository.find_user.return_value = User(id=user_id, name="Test User", email="test@example.com", age=33, gender=UserGender.MALE, phone_number="1234567890", password="testpassword")
    order_repository.find_order.return_value = Order(id=order_id, user_id=user_id, cart_id=uuid4(), total_price=100.0, type=OrderType.IN_STORE, status=OrderStatus.CONFIRMED, created_at=datetime.now(), updated_at=datetime.now(), offer_id=None)
    
    input_dto = ExecutePaymentInputDto(payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.PAYPAL_VENMO)
    
    with pytest.raises(ValueError) as excinfo:
        execute_payment_usecase.execute(order_id=order_id, user_id=user_id, input=input_dto)
    assert str(excinfo.value) == f"Order with id {order_id} already confirmed"
    user_repository.find_user.assert_called_once_with(user_id)
    order_repository.find_order.assert_called_once_with(order_id)