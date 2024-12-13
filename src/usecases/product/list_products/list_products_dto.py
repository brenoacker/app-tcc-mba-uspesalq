from typing import List
from uuid import UUID
from pydantic import BaseModel


class ListProductsInputDto(BaseModel):
    pass

class ListProductsDto(BaseModel):
    id: UUID
    name: str	
    price: float
    category: str

class ListProductsOutputDto(BaseModel):
    products: List[ListProductsDto]