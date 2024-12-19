from typing import List
from uuid import UUID

from domain.cart_item.cart_item_entity import CartItem
from domain.product.product_entity import Product


class Cart:

    id: UUID
    user_id: UUID
    total_price: float

    def __init__(self, id: UUID, user_id: UUID, total_price: float):
        self.id = id
        self.user_id = user_id
        self.total_price = total_price
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.user_id, UUID):
            raise Exception("user_id must be an UUID")

        if not isinstance(self.total_price, float) or self.total_price < 0:
            raise Exception("total_price must be a positive float")