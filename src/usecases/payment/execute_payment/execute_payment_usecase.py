import random
from datetime import datetime
from time import sleep
from uuid import UUID

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_repository_interface import OrderRepositoryInterface
from domain.order.order_status_enum import OrderStatus
from domain.payment.payment_entity import Payment
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from domain.payment.payment_status_enum import PaymentStatus
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.order.update_order.update_order_dto import UpdateOrderInputDto
from usecases.order.update_order.update_order_usecase import UpdateOrderUseCase
from usecases.payment.execute_payment.execute_payment_dto import (
    ExecutePaymentInputDto, ExecutePaymentOutputDto)


class ExecutePaymentUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface, user_repository: UserRepositoryInterface, order_repository: OrderRepositoryInterface):
        self.payment_repository = payment_repository
        self.user_repository = user_repository
        self.order_repository = order_repository

    def execute(self, order_id: UUID, user_id: UUID, input: ExecutePaymentInputDto) -> ExecutePaymentOutputDto:

        user = self.user_repository.find_user(user_id)

        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        
        order = self.order_repository.find_order(order_id=order_id, user_id=user_id)
        
        if order is None:
            raise ValueError(f"Order with id {order_id} not found")
        
        if order.status == OrderStatus.CONFIRMED:
            raise ValueError(f"Order with id {order_id} already confirmed:\n order.id: {order.id}\n order.cart_id: {order.cart_id}\n order.status: {order.status}\n order.type: {order.type}\n order.total_price: {order.total_price}\n order.offer_id: {order.offer_id}")

        payment_found = self.payment_repository.find_payment_by_order_id(order_id=order_id)

        if payment_found is None:
            raise ValueError(f"Payment for order with id {order_id} not found")
        
        if payment_found.status == PaymentStatus.PAID:
            raise ValueError(f"Payment for order with id {order_id} already paid")

        payment = Payment(
            id=payment_found.id,
            user_id=payment_found.user_id,
            order_id=payment_found.order_id, 
            payment_method=input.payment_method,
            payment_card_gateway=input.payment_card_gateway,
            status=PaymentStatus.PAID
        )

        executed_payment = self.payment_repository.execute_payment(payment=payment)

        # Simulate payment gateway processing
        sleep(1)

        # Simulate payment gateway processing for offers
        if order.offer_id is not None:
            sleep(random.randint(5,10)/10)

        return ExecutePaymentOutputDto(
            id=executed_payment.id, 
            user_id=executed_payment.user_id,
            order_id=executed_payment.order_id, 
            payment_method=executed_payment.payment_method, 
            payment_card_gateway=executed_payment.payment_card_gateway,
            status=executed_payment.status
        )
