from uuid import UUID

from pydantic import BaseModel

from domain.product.product_category_enum import ProductCategory


class FindProductInputDto(BaseModel):
    id: int

class FindProductOutputDto(BaseModel):
    id: int
    name: str	
    price: float
    category: ProductCategory