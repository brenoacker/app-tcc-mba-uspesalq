from uuid import UUID
from pydantic import BaseModel


class RemoveOrderItemInputDto(BaseModel):
    id: UUID

class RemoveOrderItemOutputDto(BaseModel):
    pass
