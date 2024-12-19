from uuid import UUID

from pydantic import BaseModel


class FindItemInputDto(BaseModel):
    id: UUID

class FindItemOutputDto(BaseModel):
    id: UUID
    cart_id: UUID
    product_id: int
    quantity: int