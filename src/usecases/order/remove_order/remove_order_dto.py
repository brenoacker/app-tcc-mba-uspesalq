from uuid import UUID

from pydantic import BaseModel


class RemoveOrderInputDto(BaseModel):
    id: UUID

class RemoveOrderOutputDto(BaseModel):
    id: UUID