from uuid import UUID
from pydantic import BaseModel


class FindProductInputDto(BaseModel):
    id: UUID

class FindProductOutputDto(BaseModel):
    id: UUID
    name: str	
    price: float
    category: str