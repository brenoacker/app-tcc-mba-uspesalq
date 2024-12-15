from typing import List
from uuid import UUID

from pydantic import BaseModel

from usecases.cart.add_cart.add_cart_dto import CartItemDto


class FindCartInputDto(BaseModel):
    user_id: UUID

class FindCartOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    items: List[CartItemDto]
    total_price: float