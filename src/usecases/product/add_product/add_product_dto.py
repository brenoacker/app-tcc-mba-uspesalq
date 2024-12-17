from uuid import UUID

from pydantic import BaseModel

from domain.product.product_category_enum import ProductCategory


class AddProductInputDto(BaseModel):
    name: str
    price: float
    category: ProductCategory

class AddProductOutputDto(BaseModel):
    id: UUID
    product_code: int
    name: str
    price: float
    category: ProductCategory