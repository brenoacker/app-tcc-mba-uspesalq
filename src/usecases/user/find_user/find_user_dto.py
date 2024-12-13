from uuid import UUID
from pydantic import BaseModel


class FindUserInputDto(BaseModel):
    id: UUID

class FindUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str
    password: str
