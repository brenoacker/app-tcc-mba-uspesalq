from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType


class ListOrdersInputDto(BaseModel):
    user_id: UUID

class ListOrderDto(BaseModel):
    id: UUID
    user_id: UUID
    cart_id: UUID
    offer_id: int = None
    total_price: float
    type: OrderType
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

class ListOrdersOutputDto(BaseModel):
    orders: List[ListOrderDto]