import json
import threading

from fastapi import Depends
from requests import Session as ReqSession
from sqlalchemy.orm import Session

from infrastructure.api.database import SessionLocal, get_session
from infrastructure.messaging.connection import get_rabbit_connection
from infrastructure.order.sqlalchemy.order_model import OrderModel


# Função para atualizar o status do pedido
def update_order_status(order_id: str, status: str, session: Session):
    print(f"Updating order {order_id} to status {status}")
    session.query(OrderModel).filter(OrderModel.id == order_id).update({"status": status})
    session.commit()


# Função que consome as mensagens do RabbitMQ
def start_consumer(queue_name: str):
    # Criação manual da sessão do banco de dados
    session = SessionLocal()  # Criar a sessão diretamente
    
    connection = get_rabbit_connection()
    channel = connection.channel()
    
    # Declara a fila
    channel.queue_declare(queue=queue_name, durable=True)
    
    def callback(ch, method, properties, body):
        message = json.loads(body)
        order_id = message["order_id"]
        status = message["status"]
        try:
            update_order_status(order_id, status, session)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print(" [*] Waiting for messages.")
    channel.start_consuming()


# Função para rodar o consumidor em uma thread
def run_consumer_thread():
    consumer_thread = threading.Thread(target=start_consumer, args=("order_queue",))  # Passa apenas o nome da fila
    consumer_thread.start()