from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, Numeric,
                        String, TypeDecorator)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from infrastructure.api.database import Base


class OrderStatusType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, OrderStatus):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return OrderStatus(value)
        return value
    
class OrderTType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, OrderType):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return OrderType(value)
        return value

class OrderModel(Base):
    __tablename__ = "tb_orders"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("tb_users.id"), nullable=False)
    cart_id = Column(UUID, ForeignKey("tb_carts.id", ondelete="CASCADE"), nullable=False)
    offer_id = Column(Integer, ForeignKey("tb_offers.id"), nullable=True)
    type = Column(OrderTType, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(OrderStatusType, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    