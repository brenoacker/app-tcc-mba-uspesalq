import random
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from infrastructure.product.sqlalchemy.product_model import ProductModel
from infrastructure.product.sqlalchemy.product_repository import \
    ProductRepository
from usecases.product.list_products.list_products_dto import ListProductsDto


@pytest.fixture
def session():
    return MagicMock()

@pytest.fixture
def product_repository(session):
    return ProductRepository(session)

def test_add_product(product_repository, session):
    product_id = random.randint(1,20)
    product = Product(
        id=product_id,
        name="Product A",
        price=10.0,
        category=ProductCategory.BURGER
    )

    added_product = product_repository.add_product(product)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert added_product.id == product.id
    assert added_product.name == product.name
    assert added_product.price == product.price
    assert added_product.category == product.category

def test_find_product(product_repository, session):
    product_id = random.randint(1,20)
    product_model = ProductModel(
        id=product_id,
        name="Product A",
        price=10.0,
        category=ProductCategory.BURGER
    )
    session.query().get.return_value = product_model

    found_product = product_repository.find_product(product_id)

    assert found_product.id == product_id
    assert found_product.name == product_model.name
    assert found_product.price == product_model.price
    assert found_product.category == product_model.category

def test_find_product_not_found(product_repository, session):
    product_id = random.randint(1,20)
    session.query().get.return_value = None

    found_product = product_repository.find_product(product_id)

    assert found_product is None

def test_find_product_by_name(product_repository, session):
    product_id = random.randint(1,20)
    name = "Product A"
    product_model = ProductModel(
        id=product_id,
        name=name,
        price=10.0,
        category=ProductCategory.BURGER
    )
    session.query().filter().first.return_value = product_model

    found_product = product_repository.find_product_by_name(name)

    assert found_product.id == product_id
    assert found_product.name == product_model.name
    assert found_product.price == product_model.price
    assert found_product.category == product_model.category

def test_find_product_by_name_not_found(product_repository, session):
    name = "Product A"
    session.query().filter().first.return_value = None

    found_product = product_repository.find_product_by_name(name)

    assert found_product is None

def test_update_product(product_repository, session):
    product_id = random.randint(1,20)
    product = Product(
        id=product_id,
        name="Product A",
        price=15.0,
        category=ProductCategory.BURGER
    )

    product_repository.update_product(product)

    session.query().filter().update.assert_called_once()
    session.commit.assert_called_once()

def test_list_products(product_repository, session):
    product_model_1 = ProductModel(
        id=random.randint(1,20),
        name="Product A",
        price=10.0,
        category=ProductCategory.BURGER
    )
    product_model_2 = ProductModel(
        id=random.randint(1,20),
        name="Product B",
        price=20.0,
        category=ProductCategory.SIDE_DISH
    )
    session.query().all.return_value = [product_model_1, product_model_2]

    products = product_repository.list_products()

    assert len(products) == 2
    assert products[0].id == product_model_1.id
    assert products[1].id == product_model_2.id

def test_delete_product(product_repository, session):
    product_id = random.randint(1,20)

    product_repository.delete_product(product_id)

    session.query().filter().delete.assert_called_once()
    session.commit.assert_called_once()

def test_delete_all_products_success(product_repository, session):
    # Act
    result = product_repository.delete_all_products()

    # Assert
    session.query(ProductModel).delete.assert_called_once()
    session.commit.assert_called_once()
    assert result is None