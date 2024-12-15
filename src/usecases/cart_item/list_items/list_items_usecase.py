from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from usecases.cart_item.add_item.cart_item_dto import CartItemInputDto
from usecases.cart_item.list_items.list_items_dto import (ListItemsInputDto,
                                                          ListItemsOutputDto)


class ListItemsUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    def execute(self, input: ListItemsInputDto) -> ListItemsOutputDto:
        
        items = self.cart_item_repository.list_items()

        return ListItemsOutputDto(items=items)