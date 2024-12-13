from uuid import UUID
from pydantic import BaseModel


class RemoveItemInputDto(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int

class RemoveItemOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int