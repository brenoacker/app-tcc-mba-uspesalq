from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.cart_item.cart_item_repository_interface import CartItemRepositoryInterface
from src.usecases.cart_item.find_item.find_item_dto import FindItemInputDto, FindItemOutputDto


class FindItemUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    def execute(self, input: FindItemInputDto) -> FindItemOutputDto:

        cart_item = self.cart_item_repository.find_item(item_id=input.id)

        return FindItemOutputDto(id=cart_item.id, user_id=cart_item.user_id, product_id=cart_item.product_id, quantity=cart_item.quantity)