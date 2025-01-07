from datetime import datetime

from pydantic import BaseModel

from domain.offer.offer_type_enum import OfferType


class AddOfferInputDto(BaseModel):
    id: int
    discount_type: OfferType
    discount_value: float
    expiration_days: int

class AddOfferOutputDto(BaseModel):
    id: int
    discount_type: OfferType
    discount_value: float
    start_date: datetime
    end_date: datetime