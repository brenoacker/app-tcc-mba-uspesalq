from uuid import UUID

from pydantic import BaseModel


class UpdateUserInputDto(BaseModel):
    name: str = None
    email: str = None
    phone_number: str = None
    password: str = None

class UpdateUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str
    password: str
