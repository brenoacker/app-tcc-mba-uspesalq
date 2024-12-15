from usecases.order_item.list_order_items.list_order_items_dto import (
    ListOrderItemsInputDto, ListOrderItemsOutputDto)

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order_item.order_item_repository_interface import \
    OrderItemRepositoryInterface
from usecases.order_item.remove_order_item.remove_order_item_dto import (
    RemoveOrderItemInputDto, RemoveOrderItemOutputDto)


class RemoveOrderItemUseCase(UseCaseInterface):
    def __init__(self, order_item_repository: OrderItemRepositoryInterface):
        self.order_item_repository = order_item_repository

    def execute(self, input: RemoveOrderItemInputDto) -> RemoveOrderItemOutputDto:
        
        self.order_item_repository.remove_order_item(order_item_id=input.id)

        return RemoveOrderItemOutputDto()