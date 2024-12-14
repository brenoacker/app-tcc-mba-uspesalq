from uuid import UUID
from pydantic import BaseModel


class FindItemInputDto(BaseModel):
    id: UUID

class FindItemOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int