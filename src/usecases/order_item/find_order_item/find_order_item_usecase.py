from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.order_item.order_item_repository_interface import OrderItemRepositoryInterface
from src.usecases.order_item.find_order_item.find_order_item_dto import FindOrderItemInputDto, FindOrderItemOutputDto


class FindOrderItemUseCase(UseCaseInterface):
    def __init__(self, order_item_repository: OrderItemRepositoryInterface):
        self.order_item_repository = order_item_repository

    def execute(self, input: FindOrderItemInputDto) -> FindOrderItemOutputDto:

        order_item = self.order_item_repository.find_order_item(order_item_id=input.id)

        return FindOrderItemOutputDto(id=order_item.id, order_id=order_item.order_id, product_id=order_item.product_id, quantity=order_item.quantity, price=order_item.price)