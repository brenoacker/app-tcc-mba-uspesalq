from uuid import UUID
from pydantic import BaseModel


class AddProductInputDto(BaseModel):
    name: str
    quantity: int
    price: float
    category: str

class AddProductOutputDto(BaseModel):
    id: UUID
    name: str
    quantity: int
    price: float
    category: str