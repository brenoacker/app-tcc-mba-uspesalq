from typing import List
from uuid import UUID

from pydantic import BaseModel


class FindCartItemsInputDto(BaseModel):
    cart_id: UUID
    user_id: UUID

class FindCartItemDto(BaseModel):
    id: UUID
    product_id: int
    quantity: int

class FindCartItemsOutputDto(BaseModel):
    items: List[FindCartItemDto]