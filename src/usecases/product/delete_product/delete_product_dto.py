from uuid import UUID

from pydantic import BaseModel


class DeleteProductInputDto(BaseModel):
    id: UUID

class DeleteProductOutputDto(BaseModel):
    id: UUID
