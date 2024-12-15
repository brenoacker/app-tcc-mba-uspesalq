from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.order_item.order_item_repository_interface import OrderItemRepositoryInterface
from src.usecases.order_item.update_order_item.update_order_item_dto import UpdateOrderItemInputDto, UpdateOrderItemOutputDto


class UpdateOrderItemUseCase(UseCaseInterface):
    def __init__(self, order_item_repository: OrderItemRepositoryInterface):
        self.order_item_repository = order_item_repository

    def execute(self, input: UpdateOrderItemInputDto) -> UpdateOrderItemOutputDto:
        
        order_item = self.order_item_repository.find_order_item(order_item_id=input.id)
        order_item.quantity = input.quantity
        order_item.price = input.price
        
        updated_order_item = self.order_item_repository.update_order_item(order_item=order_item)
        
        return UpdateOrderItemOutputDto(id=updated_order_item.id, order_id=updated_order_item.order_id, product_id=updated_order_item.product_id, quantity=updated_order_item.quantity, price=updated_order_item.price)