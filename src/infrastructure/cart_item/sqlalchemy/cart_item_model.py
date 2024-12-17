from sqlalchemy import (Column, Float, ForeignKey, Integer, String,
                        TypeDecorator)
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.api.database import Base


class CartItemModel(Base):
    __tablename__ = "tb_cart_items"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("tb_users.id"))
    product_id = Column(UUID, ForeignKey("tb_products.id"))
    quantity = Column(Integer)
