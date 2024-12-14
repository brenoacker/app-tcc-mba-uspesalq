from typing import List
from uuid import UUID
from pydantic import BaseModel
from src.domain.cart.cart_entity import Cart

class CartItemDto(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int

class AddCartInputDto(BaseModel):
    user_id: UUID
    items: List[Cart]
    total_price: float

class AddCartOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    items: List[CartItemDto]
    total_price: float