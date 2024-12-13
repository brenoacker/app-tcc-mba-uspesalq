from pydantic import BaseModel

class UpdateProductInputDto(BaseModel):
    id: int
    name: str
    price: float
    category: str

class UpdateProductOutputDto(BaseModel):
    id: int
    name: str
    price: float
    category: str
    