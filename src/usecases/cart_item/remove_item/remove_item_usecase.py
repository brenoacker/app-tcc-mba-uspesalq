from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.cart_item.cart_item_repository_interface import CartItemRepositoryInterface
from src.usecases.cart_item.remove_item.remove_item_dto import RemoveItemInputDto, RemoveItemOutputDto


class RemoveItemUseCase(UseCaseInterface):

    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    def execute(self, input: RemoveItemInputDto) -> RemoveItemOutputDto:
        
        cart_item = self.cart_item_repository.find_item(item_id=input.id)

        self.cart_item_repository.remove_item(item=cart_item)

        return None