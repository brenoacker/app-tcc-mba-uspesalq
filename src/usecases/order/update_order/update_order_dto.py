from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from usecases.order.create_order.create_order_dto import (OrderItemDto,
                                                          OrderStatusDto)


class UpdateOrderInputDto(BaseModel):
    id: UUID
    user_id: UUID
    offer_id: UUID
    type: OrderType
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

class UpdateOrderOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    offer_id: UUID
    type: OrderType
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
