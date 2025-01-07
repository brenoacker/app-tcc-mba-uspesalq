
import json

import pika

from .connection import get_rabbit_connection


def publish_message(queue_name: str, message: dict):
    connection = get_rabbit_connection()
    channel = connection.channel()
    
    # Declara a fila
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Publica a mensagem
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # Persistência
    )
    print(f" [x] Sent: {message}")
    connection.close()
