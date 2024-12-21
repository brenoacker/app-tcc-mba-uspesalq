from typing import List
from uuid import UUID

from pydantic import BaseModel

from domain.user.user_gender_enum import UserGender


class ListUsersInputDto(BaseModel):
    pass

class UserDto(BaseModel):
    id: UUID = None
    name: str = None
    email: str = None
    age: int = None
    gender: UserGender = None
    phone_number: str = None
    password: str = None

class ListUsersOutputDto(BaseModel):
    users: List[UserDto]
    