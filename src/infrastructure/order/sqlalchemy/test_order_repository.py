from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from domain.order.order_entity import Order
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from infrastructure.order.sqlalchemy.order_model import OrderModel
from infrastructure.order.sqlalchemy.order_repository import OrderRepository


@pytest.fixture
def session():
    return MagicMock()

@pytest.fixture
def order_repository(session):
    return OrderRepository(session)

def test_create_order(order_repository, session):
    order = Order(
        id=uuid4(),
        user_id=uuid4(),
        cart_id=uuid4(),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    created_order = order_repository.create_order(order)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    assert created_order.id == order.id

def test_find_order(order_repository, session):
    order_id = uuid4()
    user_id = uuid4()
    order_model = OrderModel(
        id=order_id,
        user_id=user_id,
        cart_id=uuid4(),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.query().filter().first.return_value = order_model

    found_order = order_repository.find_order(order_id, user_id)

    assert found_order.id == order_id
    assert found_order.user_id == user_id

def test_update_order(order_repository, session):
    order = Order(
        id=uuid4(),
        user_id=uuid4(),
        cart_id=uuid4(),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    updated_order = order_repository.update_order(order)

    session.query().filter().update.assert_called_once()
    session.commit.assert_called_once()
    assert updated_order.id == order.id

def test_remove_order(order_repository, session):
    order_id = uuid4()
    user_id = uuid4()
    order = Order(
        id=order_id,
        user_id=user_id,
        cart_id=uuid4(),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.query().filter().first.return_value = order

    removed_order_id = order_repository.remove_order(order_id, user_id)

    session.delete.assert_called_once()
    session.commit.assert_called_once()
    assert removed_order_id == order_id

def test_find_order_without_order_found(order_repository, session):
    order_id = uuid4()
    user_id = uuid4()
    session.query().filter().first.return_value = None

    found_order = order_repository.find_order(order_id, user_id)

    assert found_order is None

def test_find_order_by_cart_id(order_repository, session):
    cart_id = uuid4()
    order_model = OrderModel(
        id=uuid4(),
        user_id=uuid4(),
        cart_id=cart_id,
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.query().filter().first.return_value = order_model

    found_order = order_repository.find_order_by_cart_id(cart_id)

    assert found_order.cart_id == cart_id

def test_find_order_by_cart_id_without_order_found(order_repository, session):
    cart_id = uuid4()
    session.query().filter().first.return_value = None

    found_order = order_repository.find_order_by_cart_id(cart_id)

    assert found_order is None

def test_list_orders(order_repository, session):
    user_id = uuid4()
    order_model = OrderModel(
        id=uuid4(),
        user_id=user_id,
        cart_id=uuid4(),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.query().filter().all.return_value = [order_model]

    orders = order_repository.list_orders(user_id)

    assert len(orders) == 1
    assert orders[0].user_id == user_id

def test_list_orders_without_orders(order_repository, session):
    user_id = uuid4()
    session.query().filter().all.return_value = None

    orders = order_repository.list_orders(user_id)

    assert orders is None

def test_list_all_orders(order_repository, session):
    order_model = OrderModel(
        id=uuid4(),
        user_id=uuid4(),
        cart_id=uuid4(),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.query().all.return_value = [order_model]

    orders = order_repository.list_all_orders()

    assert len(orders) == 1

def test_list_all_orders_without_orders(order_repository, session):
    session.query().all.return_value = None

    orders = order_repository.list_all_orders()

    assert orders is None

def test_remove_order_without_order_found(order_repository, session):
    order_id = uuid4()
    user_id = uuid4()
    session.query().filter().first.return_value = None

    removed_order_id = order_repository.remove_order(order_id, user_id)

    assert removed_order_id is None

def test_delete_all_orders(order_repository, session):
    order_model = OrderModel(
        id=str(uuid4()),
        user_id=str(uuid4()),
        cart_id=str(uuid4()),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.query().delete.return_value = 1  # Simula a deleção de 1 ordem

    deleted_orders = order_repository.delete_all_orders()

    session.query().delete.assert_called_once()
    session.commit.assert_called_once()
    assert deleted_orders is None  # delete_all_orders retorna None