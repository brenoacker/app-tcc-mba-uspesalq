from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType


class Order:
    id: UUID
    user_id: UUID
    cart_id: UUID
    type: OrderType
    offer_id: int
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: UUID, user_id: UUID, cart_id: UUID, type: OrderType, total_price: float, status: OrderStatus, created_at: datetime, updated_at: datetime, offer_id: int = None):
        self.id = id
        self.user_id = user_id
        self.offer_id = offer_id
        self.cart_id = cart_id
        self.type = type
        self.total_price = self.set_total_price(total_price)
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.validate()
    
    def set_total_price(self, total_price: float) -> float:
        if not isinstance(total_price, float):
            raise Exception("total_price must be float")
        # Converte para Decimal e define a precisão para duas casas decimais
        total_price_decimal = Decimal(total_price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        return float(total_price_decimal)
    
    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.user_id, UUID):
            raise Exception("user_id must be an UUID")
        
        if not isinstance(self.cart_id, UUID):
            raise Exception("cart_id must be an UUID")
        
        if self.total_price < 0:
            raise Exception("total_price must be a non-negative number")
        
        if not isinstance(self.status, OrderStatus):
            raise Exception("status must be an instance of OrderStatus")
        
        if not isinstance(self.created_at, datetime):
            raise Exception("created_at must be a datetime object")
        
        if not isinstance(self.updated_at, datetime):
            raise Exception("updated_at must be a datetime object")
        
        if self.offer_id is not None and not isinstance(self.offer_id, int):
            raise Exception("offer_id must be an int or None")
        
        if not isinstance(self.type, OrderType):
            raise Exception("type must be an instance of OrderType")
