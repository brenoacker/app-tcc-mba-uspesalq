from uuid import UUID

from pydantic import BaseModel

from domain.user.user_gender_enum import UserGender


class FindUserInputDto(BaseModel):
    id: UUID

class FindUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    age: int
    gender: UserGender
    phone_number: str
    password: str
