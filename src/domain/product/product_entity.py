from uuid import UUID

from domain.product.product_category_enum import ProductCategory


class Product:

    id: int
    name: str
    price: float
    category: ProductCategory

    def __init__(self, id: int, name: str, price: float, category: ProductCategory):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.validate()

    def validate(self):

        if not isinstance(self.id, int) or self.id <= 0:
            raise Exception("id must be an integer greater than 0")
        
        if not isinstance(self.name, str) or len(self.name) == 0:
            raise Exception("name is required")
        
        if not isinstance(self.price, (float, int)) or self.price < 0:
            raise Exception("price must be a non-negative number")
        
        if not isinstance(self.category, ProductCategory):
            raise Exception("category must be an instance of ProductCategory")