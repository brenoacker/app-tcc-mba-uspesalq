from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.usecases.order.create_order.create_order_dto import OrderItemDto, OrderStatusDto


class ListOrdersInputDto(BaseModel):
    id: UUID

class ListOrderDto(BaseModel):
    id: UUID
    user_id: UUID
    offer_id: UUID
    items: List[OrderItemDto]
    total_amount: float
    status: OrderStatusDto
    created_at: datetime
    updated_at: datetime

class ListOrdersOutputDto(BaseModel):
    orders: List[ListOrderDto]