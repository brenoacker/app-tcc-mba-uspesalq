import uuid
from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.cart.cart_repository_interface import CartRepositoryInterface
from src.domain.cart_item.cart_item_entity import CartItem
from src.usecases.cart_item.add_item.add_item_dto import AddItemInputDto, AddItemOutputDto


class AddItemUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    def execute(self, input: AddItemInputDto) -> AddItemOutputDto:
        cart_item = CartItem(id=uuid.uuid4(), user_id=input.user_id, product_id=input.product_id, quantity=input.quantity)

        self.cart_item_repository.add_item(item=cart_item)

        return AddItemOutputDto(id=cart_item.id, user_id=cart_item.user_id, product_id=cart_item.product_id, quantity=cart_item.quantity)