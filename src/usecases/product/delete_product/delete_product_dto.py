from pydantic import BaseModel


class DeleteProductInputDto(BaseModel):
    id: int

class DeleteProductOutputDto(BaseModel):
    id: int
