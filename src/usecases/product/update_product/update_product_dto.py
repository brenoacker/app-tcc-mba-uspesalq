from uuid import UUID
from pydantic import BaseModel

class UpdateProductInputDto(BaseModel):
    id: UUID
    name: str
    price: float
    category: str

class UpdateProductOutputDto(BaseModel):
    id: UUID
    name: str
    price: float
    category: str
    