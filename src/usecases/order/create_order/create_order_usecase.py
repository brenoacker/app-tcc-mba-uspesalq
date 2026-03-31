import asyncio
import uuid
from datetime import datetime

import requests

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_entity import Cart
from domain.cart.cart_repository_interface import CartRepositoryInterface
from domain.offer.offer_entity import Offer
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from domain.offer.offer_type_enum import OfferType
from domain.order.order_entity import Order
from domain.order.order_repository_interface import OrderRepositoryInterface
from domain.order.order_status_enum import OrderStatus
from domain.payment.payment_card_gateway_enum import PaymentCardGateway
from domain.payment.payment_entity import Payment
from domain.payment.payment_method_enum import PaymentMethod
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from domain.payment.payment_status_enum import PaymentStatus
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.order.create_order.create_order_dto import (CreateOrderInputDto,
                                                          CreateOrderOutputDto)


class CreateOrderUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface, user_repository: UserRepositoryInterface, cart_repository: CartRepositoryInterface, offer_repository: OfferRepositoryInterface, payment_repository: PaymentRepositoryInterface):
        self.order_repository = order_repository
        self.cart_repository = cart_repository
        self.user_repository = user_repository
        self.offer_repository = offer_repository
        self.payment_repository = payment_repository

    async def execute(self, user_id: uuid.UUID, input: CreateOrderInputDto) -> CreateOrderOutputDto:
        
        user = await self.user_repository.find_user(user_id=user_id)

        if not user:
            raise ValueError(f"User with id '{user_id}' not found")
        
        order_found: Order = await self.order_repository.find_order_by_cart_id(cart_id=input.cart_id)

        if order_found is not None:
            if order_found.cart_id == input.cart_id:
                raise ValueError(f"Order for cart_id '{input.cart_id}' already exists")
        
        cart: Cart = await self.cart_repository.find_cart(cart_id=input.cart_id, user_id=user_id)

        if not cart:
            raise ValueError(f"Cart with id '{input.cart_id}' not found")

        if input.offer_id is not None:
            offer = await self.offer_repository.find_offer(offer_id=input.offer_id)

            if not offer:
                raise ValueError(f"Offer with id '{input.offer_id}' not found")
            
            if not offer.is_active():
                raise ValueError(f"Offer with id '{input.offer_id}' is not active")
        
            cart.total_price = offer.apply_discount(cart.total_price)

        order = Order(id=uuid.uuid4(), user_id=user_id, cart_id=input.cart_id, total_price=cart.total_price, type=input.type, status=OrderStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), offer_id=input.offer_id)

        created_order: Order = await self.order_repository.create_order(order=order)

        if not created_order:
            raise ValueError(f"Failed to create order for cart with id '{input.cart_id}'")

        if created_order.status != OrderStatus.PENDING:
            raise ValueError(f"Order was created but with '{created_order.status}' status, not 'PENDING'")
        
        created_payment = await self.payment_repository.create_payment(payment=Payment(
            id=uuid.uuid4(), 
            user_id=user_id, 
            order_id=created_order.id, 
            payment_method=None,
            payment_card_gateway=None,
            status=PaymentStatus.PENDING
        ))

        if not created_payment:
            raise ValueError(f"Failed to create payment for order with id '{created_order.id}'")

        return CreateOrderOutputDto(
            id=created_order.id, 
            user_id=created_order.user_id, 
            cart_id=created_order.cart_id,
            offer_id=created_order.offer_id,
            type=created_order.type,
            total_price=created_order.total_price,
            status=created_order.status, 
            created_at=created_order.created_at, 
            updated_at=created_order.updated_at
        )
