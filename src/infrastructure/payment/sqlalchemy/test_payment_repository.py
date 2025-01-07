from unittest.mock import MagicMock, patch
from uuid import uuid4

import psycopg2
import pytest
from sqlalchemy.exc import OperationalError

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from infrastructure.payment.sqlalchemy.payment_model import PaymentModel
from infrastructure.payment.sqlalchemy.payment_repository import \
    PaymentRepository


@pytest.fixture
def session():
    return MagicMock()

@pytest.fixture
def payment_repository(session):
    return PaymentRepository(session)

def test_create_payment(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    created_payment = payment_repository.create_payment(payment)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    assert created_payment.id == payment.id
    assert created_payment.user_id == payment.user_id
    assert created_payment.order_id == payment.order_id
    assert created_payment.payment_method == payment.payment_method
    assert created_payment.payment_card_gateway == payment.payment_card_gateway
    assert created_payment.status == payment.status

def test_create_payment_deadlock(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    session.add.side_effect = psycopg2.errors.DeadlockDetected

    with patch('time.sleep', return_value=None):
        with pytest.raises(Exception, match="Max retries exceeded for create_payment"):
            payment_repository.create_payment(payment)

    assert session.rollback.call_count == 3

def test_create_payment_operational_error(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    session.add.side_effect = OperationalError("Operational error", None, None)

    with pytest.raises(OperationalError):
        payment_repository.create_payment(payment)

    session.rollback.assert_called_once()

def test_execute_payment_deadlock(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    session.query().filter().update.side_effect = psycopg2.errors.DeadlockDetected

    with patch('time.sleep', return_value=None):
        with pytest.raises(Exception, match="Max retries exceeded for execute_payment"):
            payment_repository.execute_payment(payment)

    assert session.rollback.call_count == 3

def test_execute_payment_operational_error(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    session.query().filter().update.side_effect = OperationalError("Operational error", None, None)

    with pytest.raises(OperationalError):
        payment_repository.execute_payment(payment)

    session.rollback.assert_called_once()

def test_execute_payment_generic_exception(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    session.query().filter().update.side_effect = Exception("Generic error")

    with pytest.raises(Exception, match="Generic error"):
        payment_repository.execute_payment(payment)

    session.rollback.assert_called_once()

def test_execute_payment(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    executed_payment = payment_repository.execute_payment(payment)

    session.query().filter().update.assert_called_once()
    session.commit.assert_called_once()
    assert executed_payment.id == payment.id
    assert executed_payment.user_id == payment.user_id
    assert executed_payment.order_id == payment.order_id
    assert executed_payment.payment_method == payment.payment_method
    assert executed_payment.payment_card_gateway == payment.payment_card_gateway
    assert executed_payment.status == payment.status

def test_find_payment(payment_repository, session):
    payment_id = uuid4()
    payment_model = PaymentModel(
        id=payment_id,
        user_id=uuid4(),
        order_id=uuid4(),
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    session.query().filter().first.return_value = payment_model

    found_payment = payment_repository.find_payment(payment_id)

    assert found_payment.id == payment_id
    assert found_payment.user_id == payment_model.user_id
    assert found_payment.order_id == payment_model.order_id
    assert found_payment.payment_method == payment_model.payment_method
    assert found_payment.payment_card_gateway == payment_model.payment_card_gateway
    assert found_payment.status == payment_model.status

def test_find_payment_not_found(payment_repository, session):
    payment_id = uuid4()
    session.query().filter().first.return_value = None

    found_payment = payment_repository.find_payment(payment_id)

    assert found_payment is None

def test_find_payment_by_order_id(payment_repository, session):
    order_id = uuid4()
    payment_model = PaymentModel(
        id=uuid4(),
        user_id=uuid4(),
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    session.query().filter().first.return_value = payment_model

    found_payment = payment_repository.find_payment_by_order_id(order_id)

    assert found_payment.id == payment_model.id
    assert found_payment.user_id == payment_model.user_id
    assert found_payment.order_id == payment_model.order_id
    assert found_payment.payment_method == payment_model.payment_method
    assert found_payment.payment_card_gateway == payment_model.payment_card_gateway
    assert found_payment.status == payment_model.status

def test_find_payment_by_order_id_not_found(payment_repository, session):
    order_id = uuid4()
    session.query().filter().first.return_value = None

    found_payment = payment_repository.find_payment_by_order_id(order_id)

    assert found_payment is None

def test_list_payments(payment_repository, session):
    user_id = uuid4()
    payment_model_1 = PaymentModel(
        id=uuid4(),
        user_id=user_id,
        order_id=uuid4(),
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    payment_model_2 = PaymentModel(
        id=uuid4(),
        user_id=user_id,
        order_id=uuid4(),
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PENDING
    )
    session.query().filter().all.return_value = [payment_model_1, payment_model_2]

    payments = payment_repository.list_payments(user_id)

    assert len(payments) == 2
    assert payments[0].id == payment_model_1.id
    assert payments[1].id == payment_model_2.id

def test_list_payments_empty(payment_repository, session):
    user_id = uuid4()
    session.query().filter().all.return_value = []

    payments = payment_repository.list_payments(user_id)

    assert payments == []

def test_list_all_payments(payment_repository, session):
    payment_model_1 = PaymentModel(
        id=uuid4(),
        user_id=uuid4(),
        order_id=uuid4(),
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    payment_model_2 = PaymentModel(
        id=uuid4(),
        user_id=uuid4(),
        order_id=uuid4(),
        payment_method=PaymentMethod.CASH,
        payment_card_gateway=None,
        status=PaymentStatus.PENDING
    )
    session.query().all.return_value = [payment_model_1, payment_model_2]

    payments = payment_repository.list_all_payments()

    assert len(payments) == 2
    assert payments[0].id == payment_model_1.id
    assert payments[1].id == payment_model_2.id

def test_list_all_payments_empty(payment_repository, session):
    session.query().all.return_value = []

    payments = payment_repository.list_all_payments()

    assert payments == []

def test_delete_all_payments(payment_repository, session):
    payment_repository.delete_all_payments()

    session.query().delete.assert_called_once()
    session.commit.assert_called_once()