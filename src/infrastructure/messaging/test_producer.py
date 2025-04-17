import json
from unittest.mock import MagicMock

import pytest

from infrastructure.messaging.producer import publish_message


@pytest.mark.asyncio
async def test_publish_message(mocker):
    # Mock the connection and channel
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mocker.patch('src.infrastructure.messaging.producer.get_rabbit_connection', return_value=mock_connection)
    mock_connection.channel.return_value = mock_channel

    # Define the queue name and message
    queue_name = 'test_queue'
    message = {'key': 'value'}

    # Call the function
    publish_message(queue_name, message)

    # Assertions
    mock_connection.channel.assert_called_once()
    mock_channel.queue_declare.assert_called_once_with(queue=queue_name, durable=True)
    mock_channel.basic_publish.assert_called_once_with(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message),
        properties=mocker.ANY  # We use mocker.ANY to ignore the exact properties
    )
    mock_connection.close.assert_called_once()