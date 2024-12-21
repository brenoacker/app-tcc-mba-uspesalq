from datetime import datetime
from uuid import UUID

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus


class Payment:

    id: UUID
    order_id: UUID
    user_id: UUID
    payment_method: PaymentMethod
    payment_card_gateway: PaymentCardGateway
    status: PaymentStatus

    def __init__(self, id: UUID, order_id: UUID, user_id: UUID, payment_method: PaymentMethod, status: PaymentStatus, payment_card_gateway: PaymentCardGateway = None):
        self.id = id
        self.order_id = order_id
        self.user_id = user_id
        self.payment_method = payment_method
        self.payment_card_gateway = payment_card_gateway
        self.status = status
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.order_id, UUID):
            raise Exception("order_id must be an UUID")
        
        if not isinstance(self.user_id, UUID):
            raise Exception("user_id must be an UUID")
        
        if not isinstance(self.payment_method, PaymentMethod):
            raise Exception("payment_method must be an instance of PaymentMethod")
        
        if self.payment_method == PaymentMethod.CARD and not isinstance(self.payment_card_gateway, PaymentCardGateway):
                raise Exception("payment_card_gateway must be an instance of PaymentCardGateway")
        
        if not isinstance(self.status, PaymentStatus):
            raise Exception("status must be an instance of PaymentStatus")
        