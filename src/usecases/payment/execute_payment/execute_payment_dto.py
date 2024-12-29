from uuid import UUID

from pydantic import BaseModel

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus


class ExecutePaymentInputDto(BaseModel):
    payment_method: PaymentMethod
    payment_card_gateway: PaymentCardGateway = None

class ExecutePaymentOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    order_id: UUID
    payment_method: PaymentMethod
    payment_card_gateway: PaymentCardGateway = None
    status: PaymentStatus