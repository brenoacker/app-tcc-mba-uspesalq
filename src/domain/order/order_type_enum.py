from enum import Enum


class OrderType(Enum):
    DELIVERY = "delivery"
    DRIVE_THRU = "drive_thru"
    IN_STORE = "in_store"
