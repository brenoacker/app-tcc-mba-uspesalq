from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from usecases.payment.find_payment.find_payment_dto import FindPaymentInputDto
from usecases.payment.find_payment.find_payment_usecase import \
    FindPaymentUseCase


@pytest.fixture
def payment_repository():
    return Mock()

@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def find_payment_usecase(payment_repository, user_repository):
    return FindPaymentUseCase(payment_repository, user_repository)


def test_find_payment_success(find_payment_usecase, payment_repository):
    payment_id = uuid4()
    user_id = uuid4()
    payment = Payment(id=payment_id, user_id=user_id, order_id=uuid4(), payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.ADYEN, status=PaymentStatus.PAID)
    payment_repository.find_payment.return_value = payment
    
    input_dto = FindPaymentInputDto(id=payment_id, user_id=user_id)
    
    output_dto = find_payment_usecase.execute(input=input_dto)
    
    assert output_dto.id == payment_id
    assert output_dto.user_id == user_id
    assert output_dto.payment_method == PaymentMethod.CARD
    assert output_dto.payment_card_gateway == PaymentCardGateway.ADYEN
    assert output_dto.status == PaymentStatus.PAID
    payment_repository.find_payment.assert_called_once_with(payment_id=payment_id)

def test_find_payment_not_found(find_payment_usecase, payment_repository):
    payment_id = uuid4()
    user_id = uuid4()
    payment_repository.find_payment.return_value = None
    
    input_dto = FindPaymentInputDto(id=payment_id, user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        find_payment_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Payment with id {payment_id} not found"
    payment_repository.find_payment.assert_called_once_with(payment_id=payment_id)

def test_find_payment_user_not_found(find_payment_usecase, user_repository):
    payment_id = uuid4()
    user_id = uuid4()
    user_repository.find_user.return_value = None
    
    input_dto = FindPaymentInputDto(id=payment_id, user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        find_payment_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"User with id {user_id} not found"
    user_repository.find_user.assert_called_once_with(user_id=user_id)