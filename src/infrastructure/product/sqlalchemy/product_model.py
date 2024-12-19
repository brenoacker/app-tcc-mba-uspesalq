from sqlalchemy import Column, Float, Integer, String, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID

from domain.product.product_category_enum import ProductCategory
from infrastructure.api.database import Base


class ProductCategoryType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, ProductCategory):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return ProductCategory(value)
        return value
    
class ProductModel(Base):
    __tablename__ = "tb_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(ProductCategoryType)
