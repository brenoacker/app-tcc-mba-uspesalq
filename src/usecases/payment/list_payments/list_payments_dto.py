from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.domain.payment.payment_card_gateway_enum import PaymentCardGateway
from src.domain.payment.payment_method_enum import PaymentMethod
from src.domain.payment.payment_status_enum import PaymentStatus


class ListPaymentsInputDto(BaseModel):
    user_id: UUID

class ListPaymentsDto(BaseModel):
    id: UUID
    order_id: UUID
    amount: float
    payment_method: PaymentMethod
    payment_card_gateway: PaymentCardGateway
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

class ListPaymentsOutputDto(BaseModel):
    payments: List[ListPaymentsDto]