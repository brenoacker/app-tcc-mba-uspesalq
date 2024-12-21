from uuid import UUID

from pydantic import BaseModel

from domain.user.user_gender_enum import UserGender


class UpdateUserInputDto(BaseModel):
    name: str = None
    email: str = None
    age: int = None
    gender: UserGender = None
    phone_number: str = None
    password: str = None

class UpdateUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    age: int
    gender: UserGender
    phone_number: str
    password: str
