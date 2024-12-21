from pydantic import BaseModel


class RemoveOfferInputDto(BaseModel):
    id: int
