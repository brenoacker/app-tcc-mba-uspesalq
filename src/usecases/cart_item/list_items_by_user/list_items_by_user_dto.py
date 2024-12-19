from typing import List
from uuid import UUID

from pydantic import BaseModel


class ListItemsByUserInputDto(BaseModel):
    user_id: UUID

class ListItemsByUserDto(BaseModel):
    id: UUID
    user_id: UUID
    product_code: int
    quantity: int

class ListItemsByUserOutputDto(BaseModel):
    items: List[ListItemsByUserDto]