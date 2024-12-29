import pytest

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product


def test_product_creation():
    product_id = 1
    name = "Test Product"
    price = 100.0
    category = ProductCategory.BURGER

    product = Product(id=product_id, name=name, price=price, category=category)

    assert product.id == product_id
    assert product.name == name
    assert product.price == price
    assert product.category == category

def test_product_invalid_id():
    name = "Test Product"
    price = 100.0
    category = ProductCategory.DESSERT

    with pytest.raises(Exception) as excinfo:
        Product(id="invalid_id", name=name, price=price, category=category)
    assert str(excinfo.value) == "id must be an integer greater than 0"

    with pytest.raises(Exception) as excinfo:
        Product(id=-1, name=name, price=price, category=category)
    assert str(excinfo.value) == "id must be an integer greater than 0"

def test_product_invalid_name():
    product_id = 1
    price = 100.0
    category = ProductCategory.DRINK

    with pytest.raises(Exception) as excinfo:
        Product(id=product_id, name="", price=price, category=category)
    assert str(excinfo.value) == "name is required"

    with pytest.raises(Exception) as excinfo:
        Product(id=product_id, name=None, price=price, category=category)
    assert str(excinfo.value) == "name is required"

def test_product_invalid_price():
    product_id = 1
    name = "Test Product"
    category = ProductCategory.SIDE_DISH

    with pytest.raises(Exception) as excinfo:
        Product(id=product_id, name=name, price=-100.0, category=category)
    assert str(excinfo.value) == "price must be a non-negative number"

    with pytest.raises(Exception) as excinfo:
        Product(id=product_id, name=name, price="invalid_price", category=category)
    assert str(excinfo.value) == "price must be a non-negative number"

def test_product_invalid_category():
    product_id = 1
    name = "Test Product"
    price = 100.0

    with pytest.raises(Exception) as excinfo:
        Product(id=product_id, name=name, price=price, category="invalid_category")
    assert str(excinfo.value) == "category must be an instance of ProductCategory"