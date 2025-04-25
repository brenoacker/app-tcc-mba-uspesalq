from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pika
import pytest

from domain.__seedwork.test_utils import run_async
from infrastructure.messaging.connection import get_rabbit_connection


@patch('src.infrastructure.messaging.connection.pika.BlockingConnection')
@patch('src.infrastructure.messaging.connection.pika.ConnectionParameters')
@patch('src.infrastructure.messaging.connection.pika.PlainCredentials')
@pytest.mark.asyncio
async def test_get_rabbit_connection(mock_plain_credentials, mock_connection_parameters, mock_blocking_connection):
    # Mock the return values
    mock_credentials = MagicMock()
    mock_plain_credentials.return_value = mock_credentials

    mock_parameters = MagicMock()
    mock_connection_parameters.return_value = mock_parameters

    mock_connection = MagicMock()
    mock_blocking_connection.return_value = mock_connection

    # Call the function
    connection = get_rabbit_connection()

    # Assertions
    mock_plain_credentials.assert_called_once_with("rabbitmq", "rabbitmq")
    # Usando ANY para parâmetros adicionais que não queremos verificar especificamente
    mock_connection_parameters.assert_called_once_with(
        host="rabbitmq", 
        port=5672, 
        credentials=mock_credentials,
        heartbeat=60,
        blocked_connection_timeout=10,
        socket_timeout=10,
        retry_delay=1,
        connection_attempts=3
    )
    mock_blocking_connection.assert_called_once_with(mock_parameters)
    assert connection == mock_connection

@patch('src.infrastructure.messaging.connection.pika.BlockingConnection', side_effect=pika.exceptions.AMQPConnectionError("Connection failed"))
@pytest.mark.asyncio
async def test_get_rabbit_connection_failure(mock_blocking_connection):
    with pytest.raises(Exception, match="Failed to connect to RabbitMQ after several attempts"):
        get_rabbit_connection()

    assert mock_blocking_connection.call_count == 5
