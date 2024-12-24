from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from usecases.payment.list_payments.list_payments_dto import (
    ListPaymentsInputDto, ListPaymentsOutputDto)
from usecases.payment.list_payments.list_payments_usecase import \
    ListPaymentsUseCase


@pytest.fixture
def payment_repository():
    return Mock()

@pytest.fixture
def list_payments_usecase(payment_repository):
    return ListPaymentsUseCase(payment_repository)

def test_list_payments_success(list_payments_usecase, payment_repository):
    user_id = uuid4()
    payment_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id, 
        user_id=user_id, 
        order_id=order_id, 
        payment_method=PaymentMethod.CARD, 
        payment_card_gateway=PaymentCardGateway.ADYEN, 
        status=PaymentStatus.PAID
    )
    payment_repository.list_payments.return_value = [payment]
    
    input_dto = ListPaymentsInputDto(user_id=user_id)
    
    output_dto = list_payments_usecase.execute(input=input_dto)
    
    assert len(output_dto.payments) == 1
    assert output_dto.payments[0].id == payment_id
    assert output_dto.payments[0].order_id == order_id
    assert output_dto.payments[0].payment_method == PaymentMethod.CARD
    assert output_dto.payments[0].payment_card_gateway == PaymentCardGateway.ADYEN
    assert output_dto.payments[0].status == PaymentStatus.PAID
    payment_repository.list_payments.assert_called_once_with(user_id=user_id)

def test_list_payments_empty(list_payments_usecase, payment_repository):
    user_id = uuid4()
    payment_repository.list_payments.return_value = []
    
    input_dto = ListPaymentsInputDto(user_id=user_id)
    
    output_dto = list_payments_usecase.execute(input=input_dto)
    
    assert len(output_dto.payments) == 0
    payment_repository.list_payments.assert_called_once_with(user_id=user_id)