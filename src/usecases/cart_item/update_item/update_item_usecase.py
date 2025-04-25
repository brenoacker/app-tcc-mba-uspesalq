from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from usecases.cart_item.update_item.update_item_dto import (
    UpdateItemInputDto, UpdateItemOutputDto)


class UpdateItemUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    async def execute(self, cart_item_id, input: UpdateItemInputDto) -> UpdateItemOutputDto:
        cart_item = await self.cart_item_repository.find_item(item_id=cart_item_id)

        if cart_item is None:
            raise ValueError(f"Cart item with id '{cart_item_id}' not found")

        cart_item.quantity = input.quantity

        await self.cart_item_repository.update_item(item=cart_item)

        return UpdateItemOutputDto(id=cart_item.id, cart_id=cart_item.cart_id, product_id=cart_item.product_id, quantity=cart_item.quantity)