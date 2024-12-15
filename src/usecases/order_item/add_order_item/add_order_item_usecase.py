import uuid

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order_item.order_item_entity import OrderItem
from domain.order_item.order_item_repository_interface import \
    OrderItemRepositoryInterface
from usecases.order_item.add_order_item.add_order_item_dto import (
    AddOrderItemInputDto, AddOrderItemOutputDto)


class AddOrderItemUseCase(UseCaseInterface):
    def __init__(self, order_item_repository: OrderItemRepositoryInterface):
        self.order_item_repository = order_item_repository

    def execute(self, input: AddOrderItemInputDto) -> AddOrderItemOutputDto:

        order_item = OrderItem(id=uuid.uuid4(), order_id=input.order_id, product_id=input.product_id, quantity=input.quantity, price=input.price)
        
        added_order_item = self.order_item_repository.add_order_item(order_item=order_item)

        return AddOrderItemOutputDto(id=added_order_item.id, order_id=added_order_item.order_id, product_id=added_order_item.product_id, quantity=added_order_item.quantity, price=added_order_item.price)