from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_repository_interface import OrderRepositoryInterface
from usecases.order.find_order.find_order_dto import (FindOrderInputDto,
                                                      FindOrderOutputDto)


class FindOrderUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    async def execute(self, input: FindOrderInputDto) -> FindOrderOutputDto:
        
        order = await self.order_repository.find_order(order_id=input.id, user_id=input.user_id)

        if order is None:
            raise ValueError(f"Order with id '{input.id}' not found")
        
        return FindOrderOutputDto(id=order.id, user_id=order.user_id, cart_id= order.cart_id, total_price=order.total_price, type=order.type ,status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)