from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from usecases.order.create_order.create_order_dto import (OrderItemDto,
                                                          OrderStatusDto)


class FindOrderInputDto(BaseModel):
    id: UUID

class FindOrderOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    offer_id: UUID
    items: List[OrderItemDto]
    total_amount: float
    status: OrderStatusDto
    created_at: datetime
    updated_at: datetime
