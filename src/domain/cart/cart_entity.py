from typing import List
from uuid import UUID

from domain.cart_item.cart_item_entity import CartItem
from domain.product.product_entity import Product


class Cart:

    id: UUID
    user_id: UUID
    items: List[CartItem]
    total_price: float

    def __init__(self, id: UUID, user_id: UUID, items: List[CartItem]):
        self.id = id
        self.user_id = user_id
        self.items = items
        self.total_price = self.calculate_total_price()
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.user_id, UUID):
            raise Exception("user_id must be an UUID")
        
        if not isinstance(self.items, list) or not all(isinstance(item, CartItem) for item in self.items):
            raise Exception("items must be a list of CartItem objects")
        
        if not isinstance(self.total_price, (float, int)) or self.total_price < 0:
            raise Exception("total_price must be a non-negative number")
        
    def calculate_total_price(self):
        self.total_price = sum(
            self.get_product_by_id(item.product_id).price * item.quantity
            for item in self.items
        )

    def get_product_by_id(self, product_id: UUID) -> Product:
        # Implementar a lógica para obter o produto pelo ID
        # Isso pode envolver uma consulta ao banco de dados ou outra fonte de dados
        pass