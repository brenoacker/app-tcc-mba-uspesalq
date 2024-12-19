from typing import List
from uuid import UUID

from pydantic import BaseModel

from domain.cart.cart_entity import Cart
from domain.product.product_entity import Product


class UpdateCartItemDto(BaseModel):
    product_id: int
    quantity: int
    
class UpdateCartInputDto(BaseModel):
    items: List[UpdateCartItemDto]

class UpdateCartOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    total_price: float