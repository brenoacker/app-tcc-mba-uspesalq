import json
import pika

from infrastructure.messaging.connection import get_rabbit_connection


def publish_message(queue_name: str, message: dict):
    """
    Publishes a message to the specified RabbitMQ queue.
    
    Args:
        queue_name: The name of the queue to publish to
        message: The message to publish (will be converted to JSON)
    """
    # Get a connection to RabbitMQ
    connection = get_rabbit_connection()
    
    # Create a channel
    channel = connection.channel()
    
    # Declare the queue (creates it if it doesn't exist)
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Set message properties
    properties = pika.BasicProperties(
        delivery_mode=2,  # make message persistent
        content_type='application/json'
    )
    
    # Publish the message
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message),
        properties=properties
    )
    
    # Close the connection
    connection.close() 