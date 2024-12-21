from decimal import ROUND_HALF_UP, Decimal
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
        self.total_price = self.set_total_price(total_price)
        self.validate()

    def set_total_price(self, total_price: float) -> float:
        if not isinstance(total_price, float) or total_price < 0:
            raise Exception("total_price must be a positive float")
        total_price_decimal = Decimal(total_price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        return float(total_price_decimal)

    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.user_id, UUID):
            raise Exception("user_id must be an UUID")
