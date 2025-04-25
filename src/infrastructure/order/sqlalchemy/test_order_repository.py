from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
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

@pytest.mark.asyncio
async def test_create_order(order_repository, session):
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
    
    # Mock the session's async methods
    session.commit = async_return(None)

    created_order = await order_repository.create_order(order)

    # Check that the session methods were called
    assert session.add.called
    assert session.commit.called
    
    # Verifica que refresh NÃO é mais chamado (otimização implementada)
    assert not session.refresh.called
    
    # Verifica que o objeto retornado é o mesmo que foi passado
    assert created_order is order
    assert created_order.id == order.id

@pytest.mark.asyncio
async def test_find_order(order_repository, session):
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
    
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = order_model

    found_order = await order_repository.find_order(order_id, user_id)

    assert found_order.id == order_id
    assert found_order.user_id == user_id

@pytest.mark.asyncio
async def test_update_order(order_repository, session):
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
    
    # Mock the session methods
    session.execute = async_return(MagicMock())
    session.commit = async_return(None)

    updated_order = await order_repository.update_order(order)

    # Verify the session methods were called
    assert session.execute.called
    assert session.commit.called
    
    # Verificar que não estamos fazendo nova consulta após o update
    # e que o objeto retornado é o mesmo que foi passado
    assert updated_order is order

@pytest.mark.asyncio
async def test_remove_order(order_repository, session):
    order_id = uuid4()
    order_model = OrderModel(
        id=order_id,
        user_id=uuid4(),
        cart_id=uuid4(),
        offer_id=1,
        type=OrderType.DELIVERY,
        total_price=100.00,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Mock the session methods
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = order_model
    session.delete = async_return(None)
    session.commit = async_return(None)

    # Only pass order_id as that's what the actual method expects
    removed_order_id = await order_repository.remove_order(order_id)

    # Verify the session methods were called
    assert session.execute.called
    assert session.delete.called
    assert session.commit.called
    assert removed_order_id == order_id

@pytest.mark.asyncio
async def test_find_order_without_order_found(order_repository, session):
    order_id = uuid4()
    user_id = uuid4()
    
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = None

    found_order = await order_repository.find_order(order_id, user_id)

    assert found_order is None

@pytest.mark.asyncio
async def test_find_order_by_cart_id(order_repository, session):
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
    
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = order_model

    found_order = await order_repository.find_order_by_cart_id(cart_id)

    assert found_order.cart_id == cart_id

@pytest.mark.asyncio
async def test_find_order_by_cart_id_without_order_found(order_repository, session):
    cart_id = uuid4()
    
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = None

    found_order = await order_repository.find_order_by_cart_id(cart_id)

    assert found_order is None

@pytest.mark.asyncio
async def test_list_orders(order_repository, session):
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
    
    # Mock para resultado da consulta de dados
    query_result = MagicMock()
    query_result.scalars.return_value.all.return_value = [order_model]
    
    # Mock para resultado da consulta count
    count_result = MagicMock()
    count_result.scalar.return_value = 1
    
    # Configura o side_effect para diferentes chamadas ao execute
    calls = []
    async def execute_side_effect(query):
        calls.append(query)
        if "COUNT" in str(query).upper() or "count" in str(query).lower():
            return count_result
        return query_result
    
    session.execute = AsyncMock(side_effect=execute_side_effect)
    
    # Executa o método a testar
    result = await order_repository.list_orders(user_id)
    
    # Verifica o resultado
    assert isinstance(result, dict)
    assert "items" in result
    assert "pagination" in result
    assert len(result["items"]) == 1
    assert result["pagination"]["page"] == 1
    assert result["pagination"]["page_size"] == 20
    assert result["pagination"]["total_count"] == 1

@pytest.mark.asyncio
async def test_list_orders_without_orders(order_repository, session):
    user_id = uuid4()
    
    # Mock para resultado da consulta de dados - vazia
    query_result = MagicMock()
    query_result.scalars.return_value.all.return_value = []
    
    # Mock para resultado da consulta count
    count_result = MagicMock()
    count_result.scalar.return_value = 0
    
    # Configura o side_effect para diferentes chamadas ao execute
    calls = []
    async def execute_side_effect(query):
        calls.append(query)
        if "COUNT" in str(query).upper() or "count" in str(query).lower():
            return count_result
        return query_result
    
    session.execute = AsyncMock(side_effect=execute_side_effect)
    
    # Executa o método a testar
    result = await order_repository.list_orders(user_id)
    
    # Verifica o resultado
    assert isinstance(result, dict)
    assert "items" in result
    assert "pagination" in result
    assert len(result["items"]) == 0
    assert result["pagination"]["page"] == 1
    assert result["pagination"]["page_size"] == 20
    assert result["pagination"]["total_count"] == 0

@pytest.mark.asyncio
async def test_list_all_orders(order_repository, session):
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
    
    # Mock para resultado da consulta de dados
    query_result = MagicMock()
    query_result.scalars.return_value.all.return_value = [order_model]
    
    # Mock para resultado da consulta count
    count_result = MagicMock()
    count_result.scalar.return_value = 1
    
    # Configura o side_effect para diferentes chamadas ao execute
    calls = []
    async def execute_side_effect(query):
        calls.append(query)
        if "COUNT" in str(query).upper() or "count" in str(query).lower():
            return count_result
        return query_result
    
    session.execute = AsyncMock(side_effect=execute_side_effect)
    
    # Executa o método a testar
    result = await order_repository.list_all_orders()
    
    # Verifica o resultado
    assert isinstance(result, dict)
    assert "items" in result
    assert "pagination" in result
    assert len(result["items"]) == 1
    assert result["pagination"]["page"] == 1
    assert result["pagination"]["page_size"] == 50
    assert result["pagination"]["total_count"] == 1

@pytest.mark.asyncio
async def test_list_all_orders_without_orders(order_repository, session):
    # Mock para resultado da consulta de dados - vazia
    query_result = MagicMock()
    query_result.scalars.return_value.all.return_value = []
    
    # Mock para resultado da consulta count
    count_result = MagicMock()
    count_result.scalar.return_value = 0
    
    # Configura o side_effect para diferentes chamadas ao execute
    calls = []
    async def execute_side_effect(query):
        calls.append(query)
        if "COUNT" in str(query).upper() or "count" in str(query).lower():
            return count_result
        return query_result
    
    session.execute = AsyncMock(side_effect=execute_side_effect)
    
    # Executa o método a testar
    result = await order_repository.list_all_orders()
    
    # Verifica o resultado
    assert isinstance(result, dict)
    assert "items" in result
    assert "pagination" in result
    assert len(result["items"]) == 0
    assert result["pagination"]["page"] == 1
    assert result["pagination"]["page_size"] == 50
    assert result["pagination"]["total_count"] == 0

@pytest.mark.asyncio
async def test_remove_order_without_order_found(order_repository, session):
    order_id = uuid4()
    
    # Mock the execute method for the query
    session.execute = async_return(MagicMock())
    session.execute.return_value.scalars.return_value.first.return_value = None

    # Only pass order_id as that's what the actual method expects
    removed_order_id = await order_repository.remove_order(order_id)

    assert removed_order_id is None

@pytest.mark.asyncio
async def test_delete_all_orders(order_repository, session):
    # Mock the session methods
    session.execute = async_return(MagicMock())
    session.commit = async_return(None)

    deleted_orders = await order_repository.delete_all_orders()

    # Verify the session methods were called
    assert session.execute.called
    assert session.commit.called
    assert deleted_orders is None  # delete_all_orders retorna None

@pytest.mark.asyncio
async def test_update_order_operation_error(order_repository, session):
    """Teste para verificar o comportamento quando ocorre erro operacional durante a atualização"""
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
    
    # Mock do session para simular erro operacional
    session.execute = AsyncMock(side_effect=Exception("Database error"))
    session.rollback = AsyncMock()

    # Deve lançar a exceção original
    with pytest.raises(Exception, match="Database error"):
        await order_repository.update_order(order)
    
    # Deve chamar rollback após erro
    session.rollback.assert_called_once()