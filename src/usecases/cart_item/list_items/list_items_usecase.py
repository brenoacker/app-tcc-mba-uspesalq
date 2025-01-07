from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from usecases.cart_item.list_items.list_items_dto import (ListItemsDto,
                                                          ListItemsOutputDto)


class ListItemsUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    def execute(self) -> ListItemsOutputDto:
        
        items = self.cart_item_repository.list_items()

        list_items = [ListItemsDto(id=item.id, cart_id=item.cart_id, product_id=item.product_id, quantity=item.quantity) for item in items]

        return ListItemsOutputDto(items=list_items)