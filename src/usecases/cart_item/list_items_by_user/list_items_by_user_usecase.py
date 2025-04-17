from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from usecases.cart_item.list_items_by_user.list_items_by_user_dto import (
    ListItemsByUserDto, ListItemsByUserInputDto, ListItemsByUserOutputDto)


class ListItemsByUserUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    async def execute(self, input: ListItemsByUserInputDto) -> ListItemsByUserOutputDto:
        
        items = await self.cart_item_repository.list_items_by_user(user_id=input.user_id)
        
        return ListItemsByUserOutputDto(items=[ListItemsByUserDto(id=item.id, cart_id=item.cart_id, product_id=item.product_id, quantity=item.quantity) for item in items])