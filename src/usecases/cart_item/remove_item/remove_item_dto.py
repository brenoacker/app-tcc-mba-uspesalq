from uuid import UUID

from pydantic import BaseModel


class RemoveItemInputDto(BaseModel):
    id: UUID


class RemoveItemOutputDto(BaseModel):
    id: UUID
