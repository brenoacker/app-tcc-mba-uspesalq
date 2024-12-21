from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType


class CreateOrderInputDto(BaseModel):
    type: OrderType
    cart_id: UUID
    offer_id: Optional[int] = None

class CreateOrderOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    cart_id: UUID
    type: OrderType
    offer_id: int = None
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime