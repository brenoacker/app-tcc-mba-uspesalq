from typing import List
from uuid import UUID

from pydantic import BaseModel

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_method_enum import PaymentMethod


class ListAllPaymentsDto(BaseModel):
    id: UUID
    order_id: UUID
    payment_method: PaymentMethod
    payment_card_gateway: PaymentCardGateway

class ListAllPaymentsOutputDto(BaseModel):
    payments: List[ListAllPaymentsDto]