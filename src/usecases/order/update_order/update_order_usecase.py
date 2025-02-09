from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_entity import Order
from domain.order.order_repository_interface import OrderRepositoryInterface
from usecases.order.update_order.update_order_dto import (UpdateOrderInputDto,
                                                          UpdateOrderOutputDto)


class UpdateOrderUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, input: UpdateOrderInputDto) -> UpdateOrderOutputDto:

        order = Order(id=input.id, user_id=input.user_id, cart_id=input.cart_id, total_price=input.total_price, type=input.type, status=input.status, created_at=input.created_at, updated_at=input.updated_at, offer_id=input.offer_id)
        
        order_found = self.order_repository.find_order(order_id=order.id)

        if order_found is None:
            raise ValueError(f"Order with id '{input.id}' not found")

        updated_order = self.order_repository.update_order(order=order)
        
        return UpdateOrderOutputDto(id=updated_order.id, user_id=updated_order.user_id, cart_id=updated_order.cart_id, total_price=updated_order.total_price, type=updated_order.type, status=updated_order.status, created_at=updated_order.created_at, updated_at=updated_order.updated_at, offer_id=updated_order.offer_id)
    