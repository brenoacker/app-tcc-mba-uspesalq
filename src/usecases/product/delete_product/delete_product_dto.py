from uuid import UUID

from pydantic import BaseModel


class DeleteProductInputDto(BaseModel):
    id: int

class DeleteProductOutputDto(BaseModel):
    id: int
