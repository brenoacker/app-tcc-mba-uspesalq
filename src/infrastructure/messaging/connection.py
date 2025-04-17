import time
import pika


def get_rabbit_connection():
    """Establishes a connection to RabbitMQ, with retry logic."""
    max_retries = 5
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            credentials = pika.PlainCredentials("rabbitmq", "rabbitmq")
            parameters = pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            return connection
        except pika.exceptions.AMQPConnectionError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise Exception("Failed to connect to RabbitMQ after several attempts") 