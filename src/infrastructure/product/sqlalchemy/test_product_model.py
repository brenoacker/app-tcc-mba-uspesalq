import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.product.product_category_enum import ProductCategory
from infrastructure.api.database import Base
from infrastructure.product.sqlalchemy.product_model import (
    ProductCategoryType, ProductModel)


@pytest.fixture
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture
def session(engine):
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_product_model_mapping(session):
    product = ProductModel(
        name="Product A",
        price=10.0,
        category=ProductCategory.BURGER
    )
    session.add(product)
    session.commit()

    retrieved_product = session.query(ProductModel).filter_by(name="Product A").first()
    assert retrieved_product is not None
    assert retrieved_product.name == "Product A"
    assert retrieved_product.price == 10.0
    assert retrieved_product.category == ProductCategory.BURGER

def test_product_category_type():
    product_category_type = ProductCategoryType()
    
    # Teste com valor do tipo ProductCategory
    assert product_category_type.process_bind_param(ProductCategory.BURGER, None) == 'BURGER'
    
    # Teste com valor do tipo string
    assert product_category_type.process_bind_param('BURGER', None) == 'BURGER'
    
    # Teste com valor None
    assert product_category_type.process_bind_param(None, None) is None
    
    # Teste com valor do tipo string
    assert product_category_type.process_result_value('BURGER', None) == ProductCategory.BURGER
    
    # Teste com valor None
    assert product_category_type.process_result_value(None, None) is None