from uuid import UUID
from pydantic import BaseModel


class AddItemInputDto(BaseModel):
    user_id: UUID
    product_id: int
    quantity: int

class AddItemOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    product_id: int
    quantity: int