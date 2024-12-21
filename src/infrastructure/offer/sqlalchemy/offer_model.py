from sqlalchemy import Column, DateTime, Float, Integer, String, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from domain.offer.offer_type_enum import OfferType
from infrastructure.api.database import Base


class OfferDiscountType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, OfferType):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return OfferType(value)
        return value

class OfferModel(Base):
    __tablename__ = 'tb_offers'

    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    discount_type = Column(OfferDiscountType, nullable=False)
    discount_value = Column(Float, nullable=False)