from uuid import UUID

from pydantic import BaseModel


class UpdateItemInputDto(BaseModel):
    quantity: int

class UpdateItemOutputDto(BaseModel):
    id: UUID
    cart_id: UUID
    product_id: int
    quantity: int