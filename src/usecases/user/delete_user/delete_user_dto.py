from uuid import UUID

from pydantic import BaseModel


class DeleteUserInputDto(BaseModel):
    id: UUID

class DeleteUserOutputDto(BaseModel):
    pass