from uuid import UUID

from pydantic import BaseModel

from domain.product.product_category_enum import ProductCategory


class FindProductInputDto(BaseModel):
    id: UUID

class FindProductOutputDto(BaseModel):
    id: UUID
    name: str	
    price: float
    category: ProductCategory