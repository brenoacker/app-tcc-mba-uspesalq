from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_entity import Cart
from domain.cart.cart_repository_interface import CartRepositoryInterface
from usecases.cart.update_cart.update_cart_dto import (UpdateCartInputDto,
                                                       UpdateCartOutputDto)


class UpdateCartUseCase(UseCaseInterface):
    def __init__(self, cart_repository: CartRepositoryInterface):
        self.cart_repository = cart_repository

    def execute(self, input: UpdateCartInputDto) -> UpdateCartOutputDto:

        cart = Cart(id=input.id, user_id=input.user_id, items=input.items, total_price=input.total_price)

        cart = self.cart_repository.update_cart(cart=cart)

        return UpdateCartOutputDto(id=cart.id, user_id=cart.user_id, items=cart.items, total_price=cart.total_price)