from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Union
from uuid import UUID

from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType


class Order:
    id: UUID
    user_id: UUID
    cart_id: UUID
    type: OrderType
    offer_id: int
    total_price: Decimal  # Changed to Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: UUID, user_id: UUID, cart_id: UUID, type: OrderType, total_price: Union[float, Decimal], status: OrderStatus, created_at: datetime, updated_at: datetime, offer_id: int = None):
        self.id = id
        self.user_id = user_id
        self.offer_id = offer_id
        self.cart_id = cart_id
        self.type = type
        # total_price will be processed by set_total_price
        self.total_price = self.set_total_price(total_price)
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.validate()
    
    def set_total_price(self, total_price: Union[float, Decimal]) -> Decimal:  # Accepts float or Decimal, returns Decimal
        if not isinstance(total_price, (float, Decimal)):
            raise TypeError("total_price must be float or Decimal")
        
        if isinstance(total_price, float):
            # Convert float to Decimal via string to maintain precision
            total_price_decimal = Decimal(str(total_price))
        else:
            total_price_decimal = total_price
            
        # Quantize to two decimal places
        quantized_price = total_price_decimal.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        return quantized_price
    
    def validate(self):
        if not isinstance(self.id, UUID):
            raise TypeError("id must be an UUID")
        
        if not isinstance(self.user_id, UUID):
            raise TypeError("user_id must be an UUID")
        
        if not isinstance(self.cart_id, UUID):
            raise TypeError("cart_id must be an UUID")
        
        # Ensure total_price is compared against Decimal(0)
        if self.total_price < Decimal('0'):
            raise ValueError("total_price must be a non-negative number")
        
        if not isinstance(self.status, OrderStatus):
            raise TypeError("status must be an instance of OrderStatus")
        
        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime object")
        
        if not isinstance(self.updated_at, datetime):
            raise TypeError("updated_at must be a datetime object")
        
        if self.offer_id is not None and not isinstance(self.offer_id, int):
            raise TypeError("offer_id must be an int or None")
        
        if not isinstance(self.type, OrderType):
            raise TypeError("type must be an instance of OrderType")
