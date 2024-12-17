from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from usecases.cart_item.list_items_by_user.list_items_by_user_dto import (
    ListItemsByUserInputDto, ListItemsByUserOutputDto)


class ListItemsByUserUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    def execute(self, input: ListItemsByUserInputDto) -> ListItemsByUserOutputDto:
        
        items = self.cart_item_repository.list_items_by_user_id(user_id=input.user_id)
        
        return ListItemsByUserOutputDto(items=items)