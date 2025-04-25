from pydantic import BaseModel

from domain.product.product_category_enum import ProductCategory


class AddProductInputDto(BaseModel):
    id: int
    name: str
    price: float
    category: ProductCategory

class AddProductOutputDto(BaseModel):
    id: int
    name: str
    price: float
    category: ProductCategory