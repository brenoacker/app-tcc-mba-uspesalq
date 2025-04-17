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
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.PAYPAL_VENMO

    payment = Payment(id=payment_id, order_id=order_id, user_id=user_id, payment_method=payment_method, payment_card_gateway=payment_card_gateway, status=PaymentStatus.PAID)

    assert payment.id == payment_id
    assert payment.order_id == order_id
    assert payment.user_id == user_id
    assert payment.payment_method == payment_method
    assert payment.payment_card_gateway == payment_card_gateway

def test_payment_creation_with_cash():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    payment_method = PaymentMethod.CASH

    payment = Payment(id=payment_id, order_id=order_id, user_id=user_id, payment_method=payment_method, status=PaymentStatus.PAID)

    assert payment.id == payment_id
    assert payment.order_id == order_id
    assert payment.user_id == user_id
    assert payment.payment_method == payment_method
    assert payment.payment_card_gateway == None

def test_payment_invalid_id():
    order_id = uuid4()
    user_id = uuid4()
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.PAYPAL_VENMO

    with pytest.raises(Exception) as excinfo:
        Payment(id="invalid_uuid", order_id=order_id, user_id=user_id, payment_method=payment_method, payment_card_gateway=payment_card_gateway, status=PaymentStatus.PAID)
    assert str(excinfo.value) == "id must be an UUID"

def test_payment_invalid_order_id():
    payment_id = uuid4()
    user_id = uuid4()
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.ADYEN

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id="invalid_uuid", user_id=user_id, payment_method=payment_method, payment_card_gateway=payment_card_gateway, status=PaymentStatus.PAID)
    assert str(excinfo.value) == "order_id must be an UUID"

def test_payment_invalid_user_id():
    payment_id = uuid4()
    order_id = uuid4()
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.ADYEN

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id="invalid_uuid", payment_method=payment_method, payment_card_gateway=payment_card_gateway, status=PaymentStatus.PAID)
    assert str(excinfo.value) == "user_id must be an UUID"

def test_payment_invalid_payment_method():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, payment_method="invalid_method", status=PaymentStatus.PAID)
    assert str(excinfo.value) == "payment_method must be an instance of PaymentMethod"

def test_payment_invalid_payment_card_gateway():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    payment_method = PaymentMethod.CARD

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, payment_method=payment_method, payment_card_gateway="invalid_gateway", status=PaymentStatus.PAID)
    assert str(excinfo.value) == "payment_card_gateway must be an instance of PaymentCardGateway"

def test_payment_with_invalid_status():
    user_id = uuid4()
    payment_id = uuid4()
    order_id = uuid4()
    payment_method = PaymentMethod.CARD
    payment_card_gateway = PaymentCardGateway.ADYEN

    with pytest.raises(Exception) as excinfo:
        Payment(id=payment_id, order_id=order_id, user_id=user_id, payment_method=payment_method, payment_card_gateway=payment_card_gateway, status="incompleted")
    assert str(excinfo.value) == "status must be an instance of PaymentStatus"
