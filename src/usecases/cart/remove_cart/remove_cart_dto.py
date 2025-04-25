from uuid import UUID

from pydantic import BaseModel


class RemoveCartInputDto(BaseModel):
    id: UUID
    user_id: UUID

class RemoveCartOutputDto(BaseModel):
    id: UUID
    user_id: UUID