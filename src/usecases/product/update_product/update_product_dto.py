from pydantic import BaseModel

from domain.product.product_category_enum import ProductCategory


class UpdateProductInputDto(BaseModel):
    id: int
    name: str
    price: float
    category: ProductCategory

class UpdateProductOutputDto(BaseModel):
    id: int
    name: str
    price: float
    category: ProductCategory
    