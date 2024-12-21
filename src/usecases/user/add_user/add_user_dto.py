from uuid import UUID

from pydantic import BaseModel

from domain.user.user_gender_enum import UserGender


class AddUserInputDto(BaseModel):
    name: str
    email: str
    age: int
    gender: UserGender
    phone_number: str
    password: str

class AddUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    age: int
    gender: UserGender
    phone_number: str
    password: str
