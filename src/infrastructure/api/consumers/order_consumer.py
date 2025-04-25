import asyncio
import json
import threading
import time
from typing import Optional

import pika
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.exceptions import AMQPConnectionError

from infrastructure.messaging.connection import get_rabbit_connection


def process_message(ch, method, properties, body):
    """Process the message received from RabbitMQ."""
    try:
        # Parse the message body
        message = json.loads(body)
        print(f"Received order update: {message}")
        
        # Add your order processing logic here
        
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        # Reject the message and don't requeue it
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


async def start_consumer_async(queue_name: str):
    """
    Start an async consumer to listen for messages on the specified queue.
    
    Args:
        queue_name: The name of the queue to consume from
    """
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        connection = None
        try:
            # Get a connection to RabbitMQ (async version would be needed here)
            connection = get_rabbit_connection()
            
            # Create a channel
            channel = connection.channel()
            
            # Declare the queue (creates it if it doesn't exist)
            channel.queue_declare(queue=queue_name, durable=True)
            
            # Set prefetch count to 1 to ensure fair dispatch
            channel.basic_qos(prefetch_count=1)
            
            # Start consuming messages
            channel.basic_consume(queue=queue_name, on_message_callback=process_message)
            
            print(f"Consumer started listening on queue: {queue_name}")
            channel.start_consuming()
            
        except AMQPConnectionError as e:
            retry_count += 1
            print(f"Failed to connect to RabbitMQ (attempt {retry_count}/{max_retries}): {e}")
            await asyncio.sleep(5)  # Non-blocking wait
        except Exception as e:
            print(f"Error in consumer: {e}")
            if connection and not connection.is_closed:
                connection.close()
            await asyncio.sleep(5)  # Non-blocking wait
        
        # If we reach this point, the connection or channel was closed
        retry_count += 1
        if retry_count < max_retries:
            print(f"Connection lost. Retrying ({retry_count}/{max_retries})...")
            await asyncio.sleep(5)  # Non-blocking wait
        else:
            print("Max retries reached. Consumer stopped.")
            break


def start_consumer(queue_name: str):
    """
    Start a consumer in a thread (backward compatible function)
    
    Args:
        queue_name: The name of the queue to consume from
    """
    # Since the consumer runs in a separate thread, we can keep using the synchronous version
    # but we'll implement a better retry strategy
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Get a connection to RabbitMQ
            connection = get_rabbit_connection()
            
            # Create a channel
            channel = connection.channel()
            
            # Declare the queue (creates it if it doesn't exist)
            channel.queue_declare(queue=queue_name, durable=True)
            
            # Set prefetch count to 1 to ensure fair dispatch
            channel.basic_qos(prefetch_count=1)
            
            # Start consuming messages
            channel.basic_consume(queue=queue_name, on_message_callback=process_message)
            
            print(f"Consumer started listening on queue: {queue_name}")
            channel.start_consuming()
            
        except AMQPConnectionError as e:
            retry_count += 1
            print(f"Failed to connect to RabbitMQ (attempt {retry_count}/{max_retries}): {e}")
            time.sleep(5)  # This is ok in a separate thread
        except Exception as e:
            print(f"Error in consumer: {e}")
            if connection and not connection.is_closed:
                connection.close()
            time.sleep(5)  # This is ok in a separate thread
        
        # If we reach this point, the connection or channel was closed
        retry_count += 1
        if retry_count < max_retries:
            print(f"Connection lost. Retrying ({retry_count}/{max_retries})...")
            time.sleep(5)  # This is ok in a separate thread
        else:
            print("Max retries reached. Consumer stopped.")
            break
