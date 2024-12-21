from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_repository_interface import OrderRepositoryInterface
from usecases.order.list_orders.list_orders_dto import (ListOrderDto,
                                                        ListOrdersInputDto,
                                                        ListOrdersOutputDto)


class ListOrdersUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, input: ListOrdersInputDto) -> ListOrdersOutputDto:

        orders = self.order_repository.list_orders(user_id=input.user_id)

        if not orders:
            return ListOrdersOutputDto(orders=[])
        
        return ListOrdersOutputDto(orders=[ListOrderDto(id=order.id, user_id=order.user_id, type=order.type, cart_id=order.cart_id, total_price=order.total_price, status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id) for order in orders])