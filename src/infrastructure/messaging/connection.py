import pika


def get_rabbit_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq",  # Nome do serviço no docker-compose
            port=5672,        # Porta padrão AMQP
            credentials=pika.PlainCredentials("rabbitmq", "rabbitmq")
        )
    )
    return connection
