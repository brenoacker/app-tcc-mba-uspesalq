import asyncio
import random
from datetime import datetime
from uuid import UUID

import aiohttp  # Usando aiohttp para requisições HTTP assíncronas em vez de requests

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from domain.order.order_entity import Order
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

    async def execute(self, order_id: UUID, user_id: UUID, input: ExecutePaymentInputDto) -> ExecutePaymentOutputDto:
        # First phase: Get all needed data sequentially to avoid session conflicts
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

        # Atualizando o payment_found ao invés de criar um novo objeto
        payment = Payment(
            id=payment_found.id,
            user_id=payment_found.user_id,
            order_id=payment_found.order_id,
            payment_method=input.payment_method,
            payment_card_gateway=input.payment_card_gateway,
            status=PaymentStatus.PAID
        )
        
        # Preparar a atualização do pedido
        updated_order = Order(
            id=order.id,
            user_id=order.user_id,
            cart_id=order.cart_id,
            offer_id=order.offer_id,
            type=order.type,
            status=OrderStatus.CONFIRMED,
            created_at=order.created_at,
            updated_at=datetime.now(),
            total_price=order.total_price
        )
        
        # Execute operations sequentially to avoid session conflicts
        payment_result = await self.payment_repository.execute_payment(payment=payment)

        order_result = await self.order_repository.update_order(order=updated_order)

        # Verificação simplificada após atualização
        if order_result is None:
            raise ValueError(f"Failed to update order with id {order_id}")

        return ExecutePaymentOutputDto(
            id=payment_result.id, 
            user_id=payment_result.user_id,
            order_id=payment_result.order_id, 
            payment_method=payment_result.payment_method, 
            payment_card_gateway=payment_result.payment_card_gateway,
            status=payment_result.status
        )
