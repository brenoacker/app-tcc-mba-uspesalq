import uuid
from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.cart.cart_entity import Cart
from src.domain.cart.cart_repository_interface import CartRepositoryInterface
from src.usecases.cart.add_cart.add_cart_dto import AddCartInputDto, AddCartOutputDto


class AddCartUseCase(UseCaseInterface):

    def __init__(self, cart_repository: CartRepositoryInterface):
        self.cart_repository = cart_repository

    def execute(self, input: AddCartInputDto) -> AddCartOutputDto:

        cart = Cart(id=uuid.uuid4(), user_id=input.user_id, items=input.items, total_price=input.total_price)

        self.cart_repository.add_cart(cart=cart)

        return AddCartOutputDto(id=cart.id, user_id=cart.user_id, items=cart.items, total_price=cart.total_price)
    