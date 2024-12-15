from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_entity import Order
from domain.order.order_repository_interface import OrderRepositoryInterface
from usecases.order.create_order.create_order_dto import (CreateOrderInputDto,
                                                          CreateOrderOutputDto)


class CreateOrderUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, input: CreateOrderInputDto) -> CreateOrderOutputDto:
        
        order = Order(id=input.id, user_id=input.user_id, items=input.items, status=input.status, created_at=input.created_at, updated_at=input.updated_at, offer_id=input.offer_id)

        created_order = self.order_repository.create_order(order=order)

        return CreateOrderOutputDto(id=created_order.id, user_id=created_order.user_id, items=created_order.items, status=created_order.status, created_at=created_order.created_at, updated_at=created_order.updated_at, offer_id=created_order.offer_id)