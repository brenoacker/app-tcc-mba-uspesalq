from uuid import UUID

from pydantic import BaseModel


class FindCartInputDto(BaseModel):
    id: UUID
    user_id: UUID

class FindCartOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    total_price: float