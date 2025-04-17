from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from usecases.cart_item.remove_item.remove_item_dto import (
    RemoveItemInputDto, RemoveItemOutputDto)


class RemoveItemUseCase(UseCaseInterface):

    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    async def execute(self, input: RemoveItemInputDto) -> RemoveItemOutputDto:
        
        cart_item = await self.cart_item_repository.find_item(item_id=input.id)

        if not cart_item:
            raise ValueError(f"Cart Item with id '{input.id}' not found")

        await self.cart_item_repository.remove_item(item_id=cart_item.id)

        return cart_item