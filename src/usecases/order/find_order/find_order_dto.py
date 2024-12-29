from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType


class FindOrderInputDto(BaseModel):
    id: UUID
    user_id: UUID

class FindOrderOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    cart_id: UUID
    type: OrderType
    offer_id: int = None
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
