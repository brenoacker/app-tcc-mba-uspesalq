from typing import List
from uuid import UUID

from pydantic import BaseModel


class ListCartsInputDto(BaseModel):
    user_id: UUID

class ListCartsDto(BaseModel):
    id: UUID
    user_id: UUID
    total_price: float

class ListCartsOutputDto(BaseModel):
    carts: List[ListCartsDto]