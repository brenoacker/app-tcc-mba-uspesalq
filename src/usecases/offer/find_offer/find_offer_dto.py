from datetime import datetime

from pydantic import BaseModel

from domain.offer.offer_type_enum import OfferType


class FindOfferInputDto(BaseModel):
    id: int

class FindOfferOutputDto(BaseModel):
    id: int
    discount_type: OfferType
    discount_value: float
    start_date: datetime
    end_date: datetime