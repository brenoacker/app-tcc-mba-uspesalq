from uuid import UUID

from pydantic import BaseModel

from domain.product.product_category_enum import ProductCategory


class UpdateProductInputDto(BaseModel):
    name: str = None
    price: float = None
    category: ProductCategory = None

class UpdateProductOutputDto(BaseModel):
    id: UUID
    name: str
    price: float
    category: ProductCategory
    