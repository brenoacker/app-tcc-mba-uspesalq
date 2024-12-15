from uuid import UUID
from pydantic import BaseModel


class FindOrderItemInputDto(BaseModel):
    id: UUID

class FindOrderItemOutputDto(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    price: float