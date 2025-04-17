from enum import Enum


class PaymentStatus(Enum):
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"