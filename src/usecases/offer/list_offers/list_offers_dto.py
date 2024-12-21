

from datetime import datetime
from typing import List

from pydantic import BaseModel

from domain.offer.offer_type_enum import OfferType


class OfferDto(BaseModel):
    id: int
    discount_type: OfferType
    discount_value: float
    start_date: datetime
    end_date: datetime

class ListOffersOutputDto(BaseModel):
    offers: List[OfferDto]