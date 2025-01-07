from domain.__seedwork.use_case_interface import UseCaseInterface
from infrastructure.order.sqlalchemy.order_repository import OrderRepository


class DeleteAllOrdersUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self) -> None:
        self.order_repository.delete_all_orders()

        return None