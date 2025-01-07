import time

import pika


def get_rabbit_connection(retries=5, delay=5):
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",  # Nome do serviço no docker-compose
                    port=5672,        # Porta padrão AMQP
                    credentials=pika.PlainCredentials("rabbitmq", "rabbitmq")
                )
            )
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection attempt {i+1} failed: {e}")
            time.sleep(delay)
    raise Exception("Failed to connect to RabbitMQ after several attempts")

if __name__ == "__main__":
    connection = get_rabbit_connection()
    print("Connected to RabbitMQ")