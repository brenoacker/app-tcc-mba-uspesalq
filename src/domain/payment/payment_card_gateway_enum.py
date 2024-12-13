from enum import Enum


class PaymentCardGateway(Enum):
    ADYEN = "adyen"
    PAYPAL_VENMO = "paypal_venmo"