from datetime import datetime

import requests

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.offer.offer_entity import Offer
from domain.offer.offer_type_enum import OfferType
from domain.order.order_entity import Order
from domain.order.order_repository_interface import OrderRepositoryInterface
from usecases.order.update_order.update_order_dto import (UpdateOrderInputDto,
                                                          UpdateOrderOutputDto)


class UpdateOrderUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    async def execute(self, input: UpdateOrderInputDto) -> UpdateOrderOutputDto:

        order = Order(id=input.id, user_id=input.user_id, cart_id=input.cart_id, total_price=input.total_price, type=input.type, status=input.status, created_at=input.created_at, updated_at=input.updated_at, offer_id=input.offer_id)
        
        order_found = await self.order_repository.find_order(order_id=order.id, user_id=input.user_id)

        if order_found is None:
            raise ValueError(f"Order with id '{input.id}' not found")
        
        input.total_price = input.total_price or order_found.total_price
        input.type = input.type or order_found.type
        input.status =input.status or order_found.status
        input.offer_id = input.offer_id or order_found.offer_id

        # # validate if offer_id is valid
        # if input.offer_id is not None:
        #     offer_data = requests.get(f"http://localhost:8000/offer/{input.offer_id}").json()

        #     if not offer_data:
        #         raise ValueError(f"Offer with id '{input.offer_id}' not found")
            
        #     offer = Offer(
        #         id=int(offer_data['id']),  # Converte para inteiro
        #         start_date=datetime.fromisoformat(offer_data['start_date']),  # Certifique-se de que o formato da data seja compatível
        #         end_date=datetime.fromisoformat(offer_data['end_date']),
        #         discount_type=OfferType(offer_data['discount_type']),  # Converte para OfferType
        #         discount_value=float(offer_data['discount_value'])  # Converte para float
        #     )            
        #     if not offer.is_active():
        #         raise ValueError(f"Offer with id '{input.offer_id}' is not active")
        

        order = Order(id=order_found.id, user_id=order_found.user_id, cart_id=order_found.cart_id, total_price=input.total_price, type=input.type, status=input.status, created_at=order_found.created_at, updated_at=datetime.now(), offer_id=input.offer_id)

        updated_order = await self.order_repository.update_order(order=order)
        
        # Adicionando verificação para evitar AttributeError quando updated_order é None
        if updated_order is None:
            raise ValueError(f"Order with id '{input.id}' not updated")
        
        return UpdateOrderOutputDto(id=updated_order.id, user_id=updated_order.user_id, cart_id=updated_order.cart_id, total_price=updated_order.total_price, type=updated_order.type, status=updated_order.status, created_at=updated_order.created_at, updated_at=updated_order.updated_at, offer_id=updated_order.offer_id)
