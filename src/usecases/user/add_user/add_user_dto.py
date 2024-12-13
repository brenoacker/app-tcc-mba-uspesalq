from uuid import UUID
from pydantic import BaseModel


class AddUserInputDto(BaseModel):
    name: str
    email: str
    phone_number: str
    password: str

class AddUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str
    password: str
