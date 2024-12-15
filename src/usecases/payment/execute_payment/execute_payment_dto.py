from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus


class ExecutePaymentInputDto(BaseModel):
    order_id: UUID
    amount: float
    payment_method: PaymentMethod
    payment_card_gateway: PaymentCardGateway

class ExecutePaymentOutputDto(BaseModel):
    id: UUID
    order_id: UUID
    amount: float
    payment_method: PaymentMethod
    payment_card_gateway: PaymentCardGateway
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime