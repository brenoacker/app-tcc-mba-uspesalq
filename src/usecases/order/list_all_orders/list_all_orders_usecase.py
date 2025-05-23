from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.order.order_repository_interface import OrderRepositoryInterface
from usecases.order.list_all_orders.list_all_orders_dto import (
    ListAllOrderDto, ListAllOrdersOutputDto)


class ListAllOrdersUseCase(UseCaseInterface):
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    async def execute(self) -> ListAllOrdersOutputDto:
        result = await self.order_repository.list_all_orders()

        if result is None or 'items' not in result or not result['items']:
            return ListAllOrdersOutputDto(orders=[])

        # Agora extraímos a lista de orders do campo 'items' do dicionário
        orders = result['items']
        
        return ListAllOrdersOutputDto(orders=[
            ListAllOrderDto(
                id=order.id, 
                user_id=order.user_id, 
                type=order.type, 
                cart_id=order.cart_id, 
                offer_id=order.offer_id, 
                total_price=order.total_price, 
                status=order.status, 
                created_at=order.created_at, 
                updated_at=order.updated_at
            ) for order in orders
        ])