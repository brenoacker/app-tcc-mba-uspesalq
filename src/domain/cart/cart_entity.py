from decimal import ROUND_HALF_UP, Decimal
from typing import Union
from uuid import UUID


class Cart:

    id: UUID
    user_id: UUID
    total_price: Decimal  # Changed to Decimal

    def __init__(self, id: UUID, user_id: UUID, total_price: Union[float, Decimal, int]):
        self.id = id
        self.user_id = user_id
        self.total_price = self.set_total_price(total_price) # Will be converted to Decimal
        self.validate()

    def set_total_price(self, total_price: Union[float, Decimal, int]) -> Decimal: # Accepts float, Decimal, or int; returns Decimal
        if not isinstance(total_price, (float, Decimal, int)):
            raise TypeError("total_price must be a number (float, Decimal, or int)")
        
        if isinstance(total_price, (float, int)):
            # Convert float/int to Decimal via string to maintain precision
            total_price_decimal = Decimal(str(total_price))
        else: # It's already a Decimal
            total_price_decimal = total_price
        
        # Check if total_price is non-negative
        if total_price_decimal < Decimal('0'):
            raise ValueError("total_price must be a non-negative number")
        
        # Quantize to two decimal places
        quantized_price = total_price_decimal.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        return quantized_price

    def validate(self):
        if not isinstance(self.id, UUID):
            raise TypeError("id must be an UUID") # Changed
        
        if not isinstance(self.user_id, UUID):
            raise TypeError("user_id must be an UUID") # Changed
        
        # Validation for total_price (type and non-negativity) is handled in set_total_price
        if not isinstance(self.total_price, Decimal):
             # This should not be reached if __init__ and set_total_price work correctly
            raise TypeError("total_price must be a Decimal after initialization")
