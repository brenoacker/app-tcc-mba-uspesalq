from uuid import UUID
from pydantic import BaseModel


class UpdateItemInputDto(BaseModel):
    id: UUID
    quantity: int

class UpdateItemOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    product_id: int
    quantity: int