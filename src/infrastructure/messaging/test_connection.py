from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.messaging.connection import get_rabbit_connection


@patch('src.infrastructure.messaging.connection.pika.BlockingConnection')
@patch('src.infrastructure.messaging.connection.pika.ConnectionParameters')
@patch('src.infrastructure.messaging.connection.pika.PlainCredentials')
def test_get_rabbit_connection(mock_plain_credentials, mock_connection_parameters, mock_blocking_connection):
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
    mock_connection_parameters.assert_called_once_with(host="rabbitmq", port=5672, credentials=mock_credentials)
    mock_blocking_connection.assert_called_once_with(mock_parameters)
    assert connection == mock_connection