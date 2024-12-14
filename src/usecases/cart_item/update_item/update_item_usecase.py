from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.cart_item.cart_item_repository_interface import CartItemRepositoryInterface
from src.usecases.cart_item.update_item.update_item_dto import UpdateItemInputDto, UpdateItemOutputDto


class UpdateItemUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    def execute(self, input: UpdateItemInputDto) -> UpdateItemOutputDto:
        cart_item = self.cart_item_repository.find_item(item_id=input.id)

        cart_item.quantity = input.quantity

        self.cart_item_repository.update_item(item=cart_item)

        return cart_item