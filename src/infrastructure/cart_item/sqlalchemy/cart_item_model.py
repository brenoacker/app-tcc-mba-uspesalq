from sqlalchemy import (Column, ForeignKey, Integer)
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.api.database import Base


class CartItemModel(Base):
    __tablename__ = "tb_cart_items"

    id = Column(UUID, primary_key=True, index=True)
    cart_id = Column(UUID, ForeignKey("tb_carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("tb_products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)