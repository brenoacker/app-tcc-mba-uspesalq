from datetime import datetime

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_entity import Order
from domain.order.order_repository_interface import OrderRepositoryInterface
from usecases.order.update_order.update_order_dto import (UpdateOrderInputDto,
                                                          UpdateOrderOutputDto)


class UpdateOrderUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, input: UpdateOrderInputDto) -> UpdateOrderOutputDto:

        order_found = self.order_repository.find_order(order_id=input.id, user_id=input.user_id)

        if order_found is None:
            raise ValueError(f"Order with id '{input.id}' not found")
        
        input.total_price = input.total_price or order_found.total_price
        input.type = input.type or order_found.type
        input.status =input.status or order_found.status
        input.offer_id = input.offer_id or order_found.offer_id
        

        order = Order(id=order_found.id, user_id=order_found.user_id, cart_id=order_found.cart_id, total_price=input.total_price, type=input.type, status=input.status, created_at=order_found.created_at, updated_at=datetime.now(), offer_id=input.offer_id)

        updated_order = self.order_repository.update_order(order=order)

        if updated_order is None:
            raise ValueError(f"Order with id '{input.id}' not updated")
        
        return UpdateOrderOutputDto(id=updated_order.id, user_id=updated_order.user_id, cart_id=updated_order.cart_id, total_price=updated_order.total_price, type=updated_order.type, status=updated_order.status, created_at=updated_order.created_at, updated_at=updated_order.updated_at, offer_id=updated_order.offer_id)
    