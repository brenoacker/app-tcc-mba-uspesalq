import asyncio
import time
from typing import Optional

import pika
import pika.exceptions
from pika.adapters.asyncio_connection import AsyncioConnection

# Variável para armazenar a conexão e reutilizá-la
_connection_cache = None
_connection_last_used = 0
_CONNECTION_TIMEOUT = 300  # 5 minutos


def get_rabbit_connection():
    """Establishes a connection to RabbitMQ, with retry logic and connection reuse."""
    global _connection_cache, _connection_last_used
    
    # Verifica se a conexão em cache ainda é válida
    current_time = time.time()
    if (_connection_cache is not None and 
        not _connection_cache.is_closed and
        current_time - _connection_last_used < _CONNECTION_TIMEOUT):
        _connection_last_used = current_time
        return _connection_cache
    
    # Se chegou aqui, precisa criar uma nova conexão
    max_retries = 5
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            credentials = pika.PlainCredentials("rabbitmq", "rabbitmq")
            parameters = pika.ConnectionParameters(
                host="rabbitmq", 
                port=5672, 
                credentials=credentials,
                heartbeat=60,  # Keepalive para evitar que a conexão caia
                blocked_connection_timeout=10,  # Timeout para conexões bloqueadas
                socket_timeout=10,  # Timeout de socket
                retry_delay=1,  # Delay entre tentativas de conexão automáticas
                connection_attempts=3  # Número de tentativas automáticas
            )
            connection = pika.BlockingConnection(parameters)
            
            # Armazena a conexão em cache
            _connection_cache = connection
            _connection_last_used = current_time
            
            return connection
        except pika.exceptions.AMQPConnectionError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise Exception("Failed to connect to RabbitMQ after several attempts")


async def get_rabbit_connection_async() -> AsyncioConnection:
    """
    Establishes an asynchronous connection to RabbitMQ, with retry logic.
    
    Returns:
        AsyncioConnection: An asynchronous connection to RabbitMQ
    
    Raises:
        Exception: If connection cannot be established after several attempts
    """
    max_retries = 5
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # Esta função é um esboço e precisaria ser implementada com base na biblioteca aio-pika
            # ou outra biblioteca assíncrona para RabbitMQ
            credentials = pika.PlainCredentials("rabbitmq", "rabbitmq")
            parameters = pika.ConnectionParameters(
                host="rabbitmq", 
                port=5672, 
                credentials=credentials,
                heartbeat=60,
                blocked_connection_timeout=10,
                socket_timeout=10
            )
            
            # Nota: Esta implementação é um placeholder.
            # Em uma implementação real, você usaria aio_pika ou outra biblioteca assíncrona
            # Por enquanto, apenas simulamos o comportamento assíncrono
            await asyncio.sleep(0.1)  # Simulando operação assíncrona
            
            # Em uma implementação real, retornaria algo como:
            # connection = await aio_pika.connect_robust(...)
            # return connection
            
            # Por ora, retornamos a conexão bloqueante com aviso
            print("WARNING: Using blocking connection in async context. Consider using a proper async RabbitMQ client.")
            return get_rabbit_connection()
        
        except pika.exceptions.AMQPConnectionError:
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                raise Exception("Failed to connect to RabbitMQ after several attempts")
