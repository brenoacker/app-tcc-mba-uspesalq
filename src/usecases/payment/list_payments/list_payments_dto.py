from typing import List
from uuid import UUID

from pydantic import BaseModel

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus


class ListPaymentsInputDto(BaseModel):
    user_id: UUID

class ListPaymentsDto(BaseModel):
    id: UUID
    order_id: UUID
    payment_method: PaymentMethod = None
    payment_card_gateway: PaymentCardGateway = None
    status: PaymentStatus

class ListPaymentsOutputDto(BaseModel):
    payments: List[ListPaymentsDto]