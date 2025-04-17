from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture
def cart_repository():
    repo = Mock()
    repo.add_cart = AsyncMock()
    repo.find_cart = AsyncMock()
    repo.update_cart = AsyncMock()
    repo.remove_cart = AsyncMock()
    repo.list_carts = AsyncMock()
    repo.delete_all_carts = AsyncMock()
    return repo


@pytest.fixture
def cart_item_repository():
    repo = Mock()
    repo.add_item = AsyncMock()
    repo.find_item = AsyncMock()
    repo.find_items_by_cart_id = AsyncMock()
    repo.update_item = AsyncMock()
    repo.remove_item = AsyncMock()
    repo.list_items = AsyncMock()
    repo.list_items_by_user = AsyncMock()
    return repo


@pytest.fixture
def user_repository():
    repo = Mock()
    repo.add_user = AsyncMock()
    repo.find_user = AsyncMock()
    repo.update_user = AsyncMock()
    repo.list_users = AsyncMock()
    repo.delete_user = AsyncMock()
    return repo


@pytest.fixture
def product_repository():
    repo = Mock()
    repo.add_product = AsyncMock()
    repo.find_product = AsyncMock()
    repo.find_product_by_name = AsyncMock()
    repo.update_product = AsyncMock()
    repo.list_products = AsyncMock()
    repo.delete_product = AsyncMock()
    repo.delete_all_products = AsyncMock()
    return repo


@pytest.fixture
def offer_repository():
    repo = Mock()
    repo.add_offer = AsyncMock()
    repo.find_offer = AsyncMock()
    repo.update_offer = AsyncMock()
    repo.remove_offer = AsyncMock()
    repo.list_offers = AsyncMock()
    repo.remove_all_offers = AsyncMock()
    return repo


@pytest.fixture
def order_repository():
    repo = Mock()
    repo.add_order = AsyncMock()
    repo.find_order = AsyncMock()
    repo.update_order = AsyncMock()
    repo.remove_order = AsyncMock()
    repo.list_orders = AsyncMock()
    repo.list_all_orders = AsyncMock()
    return repo


@pytest.fixture
def payment_repository():
    repo = Mock()
    repo.add_payment = AsyncMock()
    repo.find_payment = AsyncMock()
    repo.list_payments = AsyncMock()
    repo.list_all_payments = AsyncMock()
    return repo 