from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.order.order_repository_interface import OrderRepositoryInterface
from src.usecases.order.find_order.find_order_dto import FindOrderInputDto, FindOrderOutputDto


class FindOrderUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, input: FindOrderInputDto) -> FindOrderOutputDto:
        
        order = self.order_repository.find_order(order_id=input.id)
        
        return FindOrderOutputDto(id=order.id, user_id=order.user_id, items=order.items, status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)