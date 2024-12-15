from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_repository_interface import OrderRepositoryInterface
from usecases.order.remove_order.remove_order_dto import (RemoveOrderInputDto,
                                                          RemoveOrderOutputDto)


class RemoveOrderUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def remove_order(self, input: RemoveOrderInputDto) -> RemoveOrderOutputDto:
        
        self.order_repository.remove_order(order_id=input.id)

        return RemoveOrderOutputDto(id=input.id)
    