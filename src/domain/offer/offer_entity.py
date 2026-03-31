from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Union

from domain.offer.offer_type_enum import OfferType


class Offer:

    id: int
    discount_type: OfferType
    discount_value: Decimal  # Changed to Decimal
    start_date: datetime
    end_date: datetime
    
    def __init__(self, id: int, start_date: datetime, end_date: datetime, discount_type: OfferType, discount_value: Union[float, Decimal]):
        self.id = id
        self.discount_type = discount_type
        
        if not isinstance(discount_value, (float, Decimal)):
            raise TypeError("discount_value must be float or Decimal")
        
        # Convert discount_value to Decimal, via string if it's a float
        if isinstance(discount_value, float):
            self.discount_value = Decimal(str(discount_value))
        else:
            self.discount_value = discount_value
            
        self.start_date = start_date
        self.end_date = end_date
        self.validate()

    def validate(self):
        if not isinstance(self.id, int):
            raise TypeError("id must be an integer") # Changed from Exception
        
        if self.id <= 0:
            raise ValueError("id must be greater than 0") # Changed from Exception
        
        if not isinstance(self.discount_type, OfferType):
            raise TypeError("discount_type must be an instance of OfferType") # Changed from Exception
        
        # discount_value is now Decimal
        if not isinstance(self.discount_value, Decimal):
            # This case should ideally not be reached if __init__ does its job
            raise TypeError("discount_value must be a Decimal") 
        
        if self.discount_value < Decimal('0'):
            raise ValueError("discount_value must be a positive number") # Changed from Exception
        
        if not isinstance(self.start_date, datetime):
            raise TypeError("start_date must be a datetime object") # Changed from Exception
        
        if not isinstance(self.end_date, datetime):
            raise TypeError("end_date must be a datetime object") # Changed from Exception
        
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date") # Changed from Exception
        
        # Original validation: if self.end_date <= datetime.now(): raise Exception("end_date must be in the future")
        # This validation might be too strict if an offer can be valid today.
        # For is_active, it checks self.start_date <= datetime.now() <= self.end_date
        # Retaining original logic for now but flagging as a potential review point.
        # If an offer's end_date is exactly datetime.now(), it's technically not in the future but could be active.
        # Consider if it should be self.end_date < datetime.now() for "in the past" or if current logic is okay.
        # For now, I will keep the original logic for this specific validation.
        if self.end_date <= datetime.now():
             raise ValueError("end_date must be in the future") # Changed from Exception
        
    def is_active(self):
        now = datetime.now()
        return self.start_date <= now <= self.end_date
    
    def apply_discount(self, price: Decimal) -> Decimal: # Input and output are Decimal
        if not isinstance(price, Decimal):
            # Defensive: convert if float is passed, though Decimal is expected
            if isinstance(price, float):
                price = Decimal(str(price))
            else:
                raise TypeError("price must be a Decimal or float")

        price_quantized = price.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

        if self.discount_type == OfferType.PERCENTAGE:
            # discount_value for percentage is the percentage itself (e.g., 10 for 10%)
            if self.discount_value < Decimal('0') or self.discount_value > Decimal('100'):
                raise ValueError("Percentage discount_value must be between 0 and 100.")
            
            discount_amount = (price_quantized * self.discount_value) / Decimal('100')
            final_price = price_quantized - discount_amount
        elif self.discount_type == OfferType.AMOUNT:
            # discount_value for amount is the monetary amount to subtract
            if price_quantized < self.discount_value:
                final_price = Decimal('0.00')
            else:
                final_price = price_quantized - self.discount_value
        else:
            # Should not happen if discount_type is validated
            raise ValueError("Unknown discount type") 

        return final_price.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
