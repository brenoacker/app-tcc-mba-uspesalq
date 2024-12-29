from datetime import datetime

from domain.offer.offer_type_enum import OfferType


class Offer:

    id: int
    discount_type: OfferType
    discount_value: float
    start_date: datetime
    end_date: datetime
    
    def __init__(self, id: int, start_date: datetime, end_date: datetime, discount_type: OfferType, discount_value: float):
        self.id = id
        self.discount_type = discount_type
        self.discount_value = discount_value
        self.start_date = start_date
        self.end_date = end_date
        self.validate()

    def validate(self):

        if not isinstance(self.id, int):
            raise Exception("id must be an integer")
        
        if self.id <= 0:
            raise Exception("id must be greater than 0")
        
        if not isinstance(self.discount_type, OfferType):
            raise Exception("discount_type must be an instance of OfferType")
        
        if not isinstance(self.discount_value, float) or self.discount_value < 0:
            raise Exception("discount_value must be a positive number")
        
        if not isinstance(self.start_date, datetime):
            raise Exception("start_date must be a datetime object")
        
        if not isinstance(self.end_date, datetime):
            raise Exception("end_date must be a datetime object")
        
        if self.start_date >= self.end_date:
            raise Exception("start_date must be before end_date")
        
        if self.end_date <= datetime.now():
            raise Exception("end_date must be in the future")
        
    def is_active(self):
        return self.start_date <= datetime.now() <= self.end_date
    
    def apply_discount(self, price: float):
        if self.discount_type == OfferType.PERCENTAGE:
            return price - (price * self.discount_value / 100)
        elif self.discount_type == OfferType.AMOUNT:
            if price < self.discount_value:
                return 0
            else:
                return price - self.discount_value
        

