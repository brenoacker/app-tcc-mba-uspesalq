from typing import List
from uuid import UUID
from pydantic import BaseModel


class ListUsersInputDto(BaseModel):
    pass

class UserDto(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str
    password: str

class ListUsersOutputDto(BaseModel):
    users: List[UserDto]
    