from uuid import UUID
from pydantic import BaseModel


class UpdateUserInputDto(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str
    password: str

class UpdateUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str
    password: str
