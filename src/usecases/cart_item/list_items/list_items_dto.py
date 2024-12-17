from typing import List
from uuid import UUID

from pydantic import BaseModel

# class ListItemsInputDto(BaseModel):
#     id: UUID

class ListItemsDto(BaseModel):
    id: UUID
    user_id: UUID
    product_id: int
    quantity: int

class ListItemsOutputDto(BaseModel):
    items: List[ListItemsDto]