from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel

class OrderItemDto(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    price: float

class OrderStatusDto(BaseModel):
    status: str

class CreateOrderInputDto(BaseModel):
    user_id: UUID
    offer_id: UUID
    items: List[OrderItemDto]
    total_amount: float
    status: OrderStatusDto
    created_at: datetime
    updated_at: datetime

class CreateOrderOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    offer_id: UUID
    items: List[OrderItemDto]
    total_amount: float
    status: OrderStatusDto
    created_at: datetime
    updated_at: datetime