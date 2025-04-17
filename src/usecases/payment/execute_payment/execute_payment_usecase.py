import random
import uuid
from datetime import datetime
from time import sleep
from uuid import UUID

import requests

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from domain.order.order_repository_interface import OrderRepositoryInterface
from domain.order.order_status_enum import OrderStatus
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from domain.payment.payment_status_enum import PaymentStatus
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.payment.execute_payment.execute_payment_dto import (
    ExecutePaymentInputDto, ExecutePaymentOutputDto)


class ExecutePaymentUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface, user_repository: UserRepositoryInterface, order_repository: OrderRepositoryInterface):
        self.payment_repository = payment_repository
        self.user_repository = user_repository
        self.order_repository = order_repository

    async def execute(self, order_id: UUID, user_id: UUID, input: ExecutePaymentInputDto) -> ExecutePaymentOutputDto:

        user = await self.user_repository.find_user(user_id)

        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        
        order = await self.order_repository.find_order(order_id=order_id, user_id=user_id)

        if order is None:
            raise ValueError(f"Order with id {order_id} not found")
        
        if order.status == OrderStatus.CONFIRMED:
            raise ValueError(f"Order with id {order_id} already confirmed:\n order.id: {order.id}\n order.cart_id: {order.cart_id}\n order.status: {order.status}\n order.type: {order.type}\n order.total_price: {order.total_price}\n order.offer_id: {order.offer_id}")

        payment_found = await self.payment_repository.find_payment_by_order_id(order_id=order_id)

        if payment_found is None:
            raise ValueError(f"Payment for order with id {order_id} not found")
        
        if payment_found.status == PaymentStatus.PAID:
            raise ValueError(f"Payment for order with id {order_id} already paid")
        
        # if order.offer_id is not None:
        #     offer_data = requests.get(f"http://localhost:8000/offer/{order.offer_id}").json()
        #     offer = Offer(
        #         id=int(offer_data['id']),  # Converte para inteiro
        #         start_date=datetime.fromisoformat(offer_data['start_date']),  # Certifique-se de que o formato da data seja compatível
        #         end_date=datetime.fromisoformat(offer_data['end_date']),
        #         discount_type=OfferType(offer_data['discount_type']),  # Converte para OfferType
        #         discount_value=float(offer_data['discount_value'])  # Converte para float
        #     )            
        #     if not offer.is_active():
        #         raise ValueError(f"Offer with id '{input.offer_id}' is not active")

        #     if not offer:
        #         raise ValueError(f"Offer with id '{input.offer_id}' not found")

        payment = Payment(
            id=uuid.uuid4(),
            user_id=user_id,
            order_id=order_id, 
            payment_method=input.payment_method,
            payment_card_gateway=input.payment_card_gateway,
            status=PaymentStatus.PAID,
        )

        executed_payment = await self.payment_repository.execute_payment(payment=payment)

        order.status = OrderStatus.CONFIRMED
        updated_order = await self.order_repository.update_order(order=order)

        if updated_order is None:
            raise ValueError(f"Failed to update order with id {order_id}")
        
        if updated_order.status != OrderStatus.CONFIRMED:
            raise ValueError(f"Failed to update order status to CONFIRMED")

        # Simulate payment gateway processing
        sleep(1)

        return ExecutePaymentOutputDto(
            id=executed_payment.id, 
            user_id=executed_payment.user_id,
            order_id=executed_payment.order_id, 
            payment_method=executed_payment.payment_method, 
            payment_card_gateway=executed_payment.payment_card_gateway,
            status=executed_payment.status
        )
