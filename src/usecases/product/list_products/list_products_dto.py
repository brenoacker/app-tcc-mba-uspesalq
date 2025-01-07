from typing import List

from pydantic import BaseModel

from domain.product.product_category_enum import ProductCategory


class ListProductsInputDto(BaseModel):
    pass

class ListProductsDto(BaseModel):
    id: int
    name: str	
    price: float
    category: ProductCategory

class ListProductsOutputDto(BaseModel):
    products: List[ListProductsDto]