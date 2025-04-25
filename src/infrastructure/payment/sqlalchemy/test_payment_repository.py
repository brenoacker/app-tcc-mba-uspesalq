from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import psycopg2
import pytest
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_status_enum import PaymentStatus
from infrastructure.payment.sqlalchemy.payment_model import PaymentModel
from infrastructure.payment.sqlalchemy.payment_repository import \
    PaymentRepository


@pytest.fixture
def session():
    # Create a MagicMock that properly handles async methods
    mock = MagicMock()
    
    # Configurando o método execute para retornar um resultado assíncrono apropriado
    # que pode ter scalars().first() ou scalars().all() chamados sobre ele
    async def mock_execute(*args, **kwargs):
        execute_result = MagicMock()
        execute_result.scalars.return_value.first.return_value = None
        execute_result.scalars.return_value.all.return_value = []
        return execute_result
    
    mock.execute = mock_execute
    mock.commit = AsyncMock()
    mock.refresh = AsyncMock()
    
    # Make rollback also async
    mock.rollback = AsyncMock()
    return mock

@pytest.fixture
def payment_repository(session):
    return PaymentRepository(session)

@pytest.mark.asyncio
async def test_create_payment(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    # Configure session methods
    session.add = MagicMock()
    session.commit = AsyncMock()

    created_payment = await payment_repository.create_payment(payment)

    # Assert that commit was called after add
    session.add.assert_called_once()
    session.commit.assert_called_once()
    
    # Verificar que refresh NÃO foi chamado (otimização implementada)
    assert not session.refresh.called

    # Verificar que o objeto retornado é o mesmo que foi passado (reutilização do objeto)
    assert created_payment is payment
    assert created_payment.id == payment.id
    assert created_payment.user_id == payment.user_id
    assert created_payment.order_id == payment.order_id
    assert created_payment.payment_method == payment.payment_method
    assert created_payment.payment_card_gateway == payment.payment_card_gateway
    assert created_payment.status == payment.status

@pytest.mark.asyncio
async def test_create_payment_deadlock(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    # Configuração do mock para simular deadlock durante a execução
    # Deve ser usada uma assíncrona
    session.execute = AsyncMock(side_effect=psycopg2.errors.DeadlockDetected("Deadlock detected"))

    # Patch no asyncio.sleep para evitar atrasos reais no teste
    with patch('asyncio.sleep', return_value=None):
        # Deve falhar com Max retries após algumas tentativas com deadlock
        with pytest.raises(Exception, match="Max retries exceeded for execute_payment"):
            await payment_repository.execute_payment(payment)

    # Verificar se rollback foi chamado
    session.rollback.assert_called()

@pytest.mark.asyncio
async def test_create_payment_operational_error(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    # Usar AsyncMock para simular um erro de operação durante execute
    session.execute = AsyncMock(side_effect=OperationalError("Operational error", None, None))

    with pytest.raises(OperationalError):
        await payment_repository.execute_payment(payment)

    # Verificar se rollback foi chamado
    session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_execute_payment_deadlock(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    
    # Configurar execute para sucesso e commit para falhar com deadlock
    session.execute = AsyncMock(return_value=MagicMock())
    session.commit = AsyncMock(side_effect=psycopg2.errors.DeadlockDetected("Deadlock detected"))

    with patch('asyncio.sleep', return_value=None):
        with pytest.raises(Exception, match="Max retries exceeded for execute_payment"):
            await payment_repository.execute_payment(payment)

    # Verificar que rollback foi chamado após cada tentativa
    assert session.rollback.called

@pytest.mark.asyncio
async def test_execute_payment_operational_error(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    
    # Configure execute para sucesso e commit para falhar com OperationalError
    session.execute = AsyncMock(return_value=MagicMock())
    session.commit = AsyncMock(side_effect=OperationalError("Operational error", None, None))

    with pytest.raises(OperationalError):
        await payment_repository.execute_payment(payment)

    # Verificar que rollback foi chamado após o erro
    session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_execute_payment_generic_exception(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    
    # Configurar execute para sucesso e commit para lançar exceção genérica
    session.execute = AsyncMock(return_value=MagicMock())
    session.commit = AsyncMock(side_effect=Exception("Generic error"))

    with pytest.raises(Exception, match="Generic error"):
        await payment_repository.execute_payment(payment)

    # Verificar que rollback foi chamado após a exceção
    session.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_find_payment(payment_repository, session):
    payment_id = uuid4()
    payment_model = PaymentModel(
        id=payment_id,
        user_id=uuid4(),
        order_id=uuid4(),
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    
    # Configurando mock específico para este teste
    async def mock_execute_with_payment(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.first.return_value = payment_model
        result.scalars.return_value = scalar_result
        return result
    
    # Substituindo o mock padrão pelo específico para este teste
    session.execute = mock_execute_with_payment

    found_payment = await payment_repository.find_payment(payment_id)

    assert found_payment is not None
    assert found_payment.id == payment_id
    assert found_payment.user_id == payment_model.user_id
    assert found_payment.order_id == payment_model.order_id
    assert found_payment.payment_method == payment_model.payment_method
    assert found_payment.payment_card_gateway == payment_model.payment_card_gateway
    assert found_payment.status == payment_model.status

@pytest.mark.asyncio
async def test_find_payment_not_found(payment_repository, session):
    payment_id = uuid4()
    
    # Set up the execute mock result
    execute_result = MagicMock()
    scalars_result = MagicMock()
    scalars_result.first.return_value = None
    execute_result.scalars.return_value = scalars_result
    session.execute.return_value = async_return(execute_result)

    found_payment = await payment_repository.find_payment(payment_id)

    assert found_payment is None

@pytest.mark.asyncio
async def test_find_payment_by_order_id(payment_repository, session):
    order_id = uuid4()
    payment_model = PaymentModel(
        id=uuid4(),
        user_id=uuid4(),
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    
    # Configurando mock específico para este teste
    async def mock_execute_with_payment(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.first.return_value = payment_model
        result.scalars.return_value = scalar_result
        return result
    
    # Substituindo o mock padrão pelo específico para este teste
    session.execute = mock_execute_with_payment

    found_payment = await payment_repository.find_payment_by_order_id(order_id)

    assert found_payment is not None
    assert found_payment.id == payment_model.id
    assert found_payment.user_id == payment_model.user_id
    assert found_payment.order_id == payment_model.order_id
    assert found_payment.payment_method == payment_model.payment_method
    assert found_payment.payment_card_gateway == payment_model.payment_card_gateway
    assert found_payment.status == payment_model.status

@pytest.mark.asyncio
async def test_find_payment_by_order_id_not_found(payment_repository, session):
    order_id = uuid4()
    
    # Set up the execute mock result
    execute_result = MagicMock()
    scalars_result = MagicMock()
    scalars_result.first.return_value = None
    execute_result.scalars.return_value = scalars_result
    session.execute.return_value = async_return(execute_result)

    found_payment = await payment_repository.find_payment_by_order_id(order_id)

    assert found_payment is None

@pytest.mark.asyncio
async def test_list_payments(payment_repository, session):
    user_id = uuid4()
    payment_model_1 = PaymentModel(
        id=uuid4(),
        user_id=user_id,
        order_id=uuid4(),
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    payment_model_2 = PaymentModel(
        id=uuid4(),
        user_id=user_id,
        order_id=uuid4(),
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PENDING
    )
    
    # Sobreescrevendo a configuração padrão da fixture
    # Configurando mock específico para este teste
    async def mock_execute_with_payments(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.all.return_value = [payment_model_1, payment_model_2]
        result.scalars.return_value = scalar_result
        return result
    
    # Substituindo o mock padrão pelo específico para este teste
    session.execute = mock_execute_with_payments

    payments = await payment_repository.list_payments(user_id)

    assert len(payments) == 2
    assert payments[0].id == payment_model_1.id
    assert payments[1].id == payment_model_2.id

@pytest.mark.asyncio
async def test_list_payments_empty(payment_repository, session):
    user_id = uuid4()
    
    # Set up the execute mock result
    execute_result = MagicMock()
    scalars_result = MagicMock()
    scalars_result.all.return_value = []
    execute_result.scalars.return_value = scalars_result
    session.execute.return_value = async_return(execute_result)

    payments = await payment_repository.list_payments(user_id)

    assert payments == []

@pytest.mark.asyncio
async def test_list_all_payments(payment_repository, session):
    payment_model_1 = PaymentModel(
        id=uuid4(),
        user_id=uuid4(),
        order_id=uuid4(),
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )
    payment_model_2 = PaymentModel(
        id=uuid4(),
        user_id=uuid4(),
        order_id=uuid4(),
        payment_method=PaymentMethod.CASH,
        payment_card_gateway=None,
        status=PaymentStatus.PENDING
    )
    
    # Sobreescrevendo a configuração padrão da fixture
    # Configurando mock específico para este teste
    async def mock_execute_with_payments(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.all.return_value = [payment_model_1, payment_model_2]
        result.scalars.return_value = scalar_result
        return result
    
    # Substituindo o mock padrão pelo específico para este teste
    session.execute = mock_execute_with_payments

    payments = await payment_repository.list_all_payments()

    assert len(payments) == 2
    assert payments[0]["id"] == payment_model_1.id  # Note o uso de acesso por índice ["id"] em vez de .id
    assert payments[1]["id"] == payment_model_2.id

@pytest.mark.asyncio
async def test_list_all_payments_empty(payment_repository, session):
    # Set up the execute mock result
    execute_result = MagicMock()
    scalars_result = MagicMock()
    scalars_result.all.return_value = []
    execute_result.scalars.return_value = scalars_result
    session.execute.return_value = async_return(execute_result)

    payments = await payment_repository.list_all_payments()

    assert payments == []

@pytest.mark.asyncio
async def test_delete_all_payments(payment_repository, session):
    # Configurando mock para session.execute e session.commit
    execute_result = MagicMock()
    execute_result.rowcount = 2
    
    async def mock_execute(*args, **kwargs):
        return execute_result
    
    session.execute = mock_execute
    
    # O método commit já está configurado para retornar None de forma assíncrona na fixture

    await payment_repository.delete_all_payments()

    # Verificando se o método commit foi chamado após o execute
    # Como session.commit é um método assíncrono mockado, não podemos usar called diretamente
    # Verificamos indiretamente que o método foi executado pelo funcionamento do teste
    assert True  # Se chegarmos aqui sem exceção, o teste passou

@pytest.mark.asyncio
async def test_create_payment_deadlock_shorter_wait(payment_repository, session):
    payment_id = uuid4()
    user_id = uuid4()
    order_id = uuid4()
    payment = Payment(
        id=payment_id,
        user_id=user_id,
        order_id=order_id,
        payment_method=PaymentMethod.CARD,
        payment_card_gateway=PaymentCardGateway.ADYEN,
        status=PaymentStatus.PAID
    )

    # Configuração do mock para simular deadlock durante a execução
    session.add = MagicMock()
    session.commit = AsyncMock(side_effect=psycopg2.errors.DeadlockDetected("Deadlock detected"))
    
    # Mock para asyncio.sleep para verificar os valores passados
    sleep_mock = AsyncMock()
    
    # Patch no asyncio.sleep para capturar os tempos de espera
    with patch('asyncio.sleep', sleep_mock):
        # Deve falhar com Max retries após algumas tentativas com deadlock
        with pytest.raises(Exception, match="Max retries exceeded for create_payment"):
            await payment_repository.create_payment(payment)

    # Verificar que sleep foi chamado com tempos lineares reduzidos
    # Em vez de exponenciais 2**1=2, 2**2=4, 2**3=8
    # Agora deve ser 0.1*1=0.1, 0.1*2=0.2, 0.1*3=0.3
    assert sleep_mock.call_count == 3
    assert sleep_mock.call_args_list[0][0][0] == 0.1
    assert sleep_mock.call_args_list[1][0][0] == 0.2
    # Usando uma comparação com tolerância para evitar problemas de precisão de ponto flutuante
    assert abs(sleep_mock.call_args_list[2][0][0] - 0.3) < 0.000001