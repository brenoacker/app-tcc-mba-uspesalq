from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        TypeDecorator)
from sqlalchemy.dialects.postgresql import UUID

from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from infrastructure.api.database import Base


class PaymentMethodType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, PaymentMethod):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return PaymentMethod(value)
        return value
    
class PaymentCardGatewayType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, PaymentCardGateway):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return PaymentCardGateway(value)
        return value

class PaymentStatusType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, PaymentStatus):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return PaymentStatus(value)
        return value

class PaymentModel(Base):
    __tablename__ = 'tb_payments'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('tb_users.id'), nullable=False)
    order_id = Column(UUID, ForeignKey('tb_orders.id'), nullable=False)
    payment_method = Column(PaymentMethodType, nullable=False)
    payment_card_gateway = Column(PaymentCardGatewayType, nullable=False)
    status = Column(PaymentStatusType, nullable=False)
