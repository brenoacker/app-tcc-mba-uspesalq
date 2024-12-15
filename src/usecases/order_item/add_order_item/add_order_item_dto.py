from uuid import UUID
from pydantic import BaseModel


class AddOrderItemInputDto(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int
    price: float

class AddOrderItemOutputDto(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    price: float