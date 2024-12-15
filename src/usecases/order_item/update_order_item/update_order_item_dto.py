from uuid import UUID
from pydantic import BaseModel


class UpdateOrderItemInputDto(BaseModel):
    id: UUID
    quantity: int
    price: float

class UpdateOrderItemOutputDto(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    price: float