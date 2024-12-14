from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.order.order_repository_interface import OrderRepositoryInterface
from src.usecases.order.list_orders.list_orders_dto import ListOrdersInputDto, ListOrdersOutputDto


class ListOrdersUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, input: ListOrdersInputDto) -> ListOrdersOutputDto:

        orders = self.order_repository.list_orders(user_id=input.user_id)

        return ListOrdersOutputDto(orders=orders)