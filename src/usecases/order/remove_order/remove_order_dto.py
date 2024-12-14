from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.usecases.order.create_order.create_order_dto import OrderItemDto, OrderStatusDto


class RemoveOrderInputDto(BaseModel):
    id: UUID

class RemoveOrderOutputDto(BaseModel):
    id: UUID