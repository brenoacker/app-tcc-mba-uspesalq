from sqlalchemy import (Column, Float, ForeignKey, Integer, String,
                        TypeDecorator)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from infrastructure.api.database import Base


class CartModel(Base):
    __tablename__ = "tb_carts"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("tb_users.id"))
    total_price = Column(Float, nullable=False)