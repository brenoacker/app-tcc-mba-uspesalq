from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_repository_interface import OrderRepositoryInterface


class DeleteAllOrdersUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    async def execute(self, input=None) -> None:
        await self.order_repository.delete_all_orders()
        return None 
