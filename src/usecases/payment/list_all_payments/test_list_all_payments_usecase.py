from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from usecases.payment.list_all_payments.list_all_payments_usecase import \
    ListAllPaymentsUseCase


@pytest.fixture
def payment_repository():
    repo = Mock()
    repo.list_all_payments = AsyncMock()
    return repo

@pytest.fixture
def list_all_payments_usecase(payment_repository):
    return ListAllPaymentsUseCase(payment_repository)

@pytest.mark.asyncio
async def test_list_all_payments_success(list_all_payments_usecase, payment_repository):
    payment_id = uuid4()
    order_id = uuid4()
    payment = Payment(id=payment_id, user_id=uuid4(), order_id=order_id, payment_method=PaymentMethod.CARD, payment_card_gateway=PaymentCardGateway.ADYEN, status=PaymentStatus.PAID)
    payment_repository.list_all_payments = async_return([payment])
    
    output_dto = await list_all_payments_usecase.execute()
    
    assert len(output_dto.payments) == 1
    assert output_dto.payments[0].id == payment_id
    assert output_dto.payments[0].order_id == order_id
    assert output_dto.payments[0].payment_method == PaymentMethod.CARD
    assert output_dto.payments[0].payment_card_gateway == PaymentCardGateway.ADYEN
    payment_repository.list_all_payments.await_count == 1

@pytest.mark.asyncio
async def test_list_all_payments_empty(list_all_payments_usecase, payment_repository):
    payment_repository.list_all_payments = async_return([])
    
    output_dto = await list_all_payments_usecase.execute()
    
    assert len(output_dto.payments) == 0
    payment_repository.list_all_payments.await_count == 1

@pytest.mark.asyncio
async def test_list_all_payments_none(list_all_payments_usecase, payment_repository):
    payment_repository.list_all_payments = async_return(None)
    
    output_dto = await list_all_payments_usecase.execute()
    
    assert len(output_dto.payments) == 0
    payment_repository.list_all_payments.await_count == 1
