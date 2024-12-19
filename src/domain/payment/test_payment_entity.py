from datetime import datetime
from uuid import uuid4

import pytest

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus


def test_payment_creation_with_card():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.PAYPAL_VENMO
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    payment = Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=amount, payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at, payment_card_gateway=payment_card_gateway)

    assert payment.id == payment_id
    assert payment.order_id == order_id
    assert payment.user_id == user_id
    assert payment.amount == amount
    assert payment.payment_method == payment_method
    assert payment.payment_card_gateway == payment_card_gateway
    assert payment.status == status
    assert payment.created_at == created_at
    assert payment.updated_at == updated_at

def test_payment_creation_with_pix():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.PIX
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    payment = Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=amount, payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at)

    assert payment.id == payment_id
    assert payment.order_id == order_id
    assert payment.user_id == user_id
    assert payment.amount == amount
    assert payment.payment_method == payment_method
    assert payment.payment_card_gateway == None
    assert payment.status == status
    assert payment.created_at == created_at
    assert payment.updated_at == updated_at

def test_payment_creation_with_cash():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.CASH
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    payment = Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=amount, payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at)

    assert payment.id == payment_id
    assert payment.order_id == order_id
    assert payment.user_id == user_id
    assert payment.amount == amount
    assert payment.payment_method == payment_method
    assert payment.payment_card_gateway == None
    assert payment.status == status
    assert payment.created_at == created_at
    assert payment.updated_at == updated_at

def test_payment_invalid_id():
    order_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.PAYPAL_VENMO
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Payment(id="invalid_uuid", order_id=order_id, user_id=user_id, amount=amount, payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at, payment_card_gateway=payment_card_gateway)
    assert str(excinfo.value) == "id must be an UUID"

def test_payment_invalid_order_id():
    payment_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.ADYEN
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id="invalid_uuid", user_id=user_id, amount=amount, payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at, payment_card_gateway=payment_card_gateway)
    assert str(excinfo.value) == "order_id must be an UUID"

def test_payment_invalid_user_id():
    payment_id = uuid4()
    order_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.ADYEN
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id="invalid_uuid", amount=amount, payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at, payment_card_gateway=payment_card_gateway)
    assert str(excinfo.value) == "user_id must be an UUID"

def test_payment_invalid_amount():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.ADYEN
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=-100.0, payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at, payment_card_gateway=payment_card_gateway)
    assert str(excinfo.value) == "amount must be a positive number"

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, amount="invalid_amount", payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at, payment_card_gateway=payment_card_gateway)
    assert str(excinfo.value) == "amount must be a positive number"

def test_payment_invalid_payment_method():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=amount, payment_method="invalid_method", status=status, created_at=created_at, updated_at=updated_at)
    assert str(excinfo.value) == "payment_method must be an instance of PaymentMethod"

def test_payment_invalid_payment_card_gateway():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.CARD
    status = PaymentStatus.PENDING
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=amount, payment_method=payment_method, status=status, created_at=created_at, updated_at=updated_at, payment_card_gateway="invalid_gateway")
    assert str(excinfo.value) == "payment_card_gateway must be an instance of PaymentCardGateway"

def test_payment_invalid_status():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.ADYEN
    created_at = datetime.now()
    updated_at = datetime.now()

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=amount, payment_method=payment_method, status="invalid_status", created_at=created_at, updated_at=updated_at, payment_card_gateway=payment_card_gateway)
    assert str(excinfo.value) == "status must be an instance of PaymentStatus"

def test_payment_invalid_dates():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    amount = 100.0
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.ADYEN
    status = PaymentStatus.PENDING

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=amount, payment_method=payment_method, status=status, created_at="invalid_date", updated_at=datetime.now(), payment_card_gateway=payment_card_gateway)
    assert str(excinfo.value) == "created_at must be a datetime object"

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, amount=amount, payment_method=payment_method, status=status, created_at=datetime.now(), updated_at="invalid_date", payment_card_gateway=payment_card_gateway)
    assert str(excinfo.value) == "updated_at must be a datetime object"