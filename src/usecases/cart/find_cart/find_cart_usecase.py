from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_repository_interface import CartRepositoryInterface
from usecases.cart.find_cart.find_cart_dto import (FindCartInputDto,
                                                   FindCartOutputDto)


class FindCartUseCase(UseCaseInterface):
    def __init__(self, cart_repository: CartRepositoryInterface):
        self.cart_repository = cart_repository

    def execute(self, input: FindCartInputDto) -> FindCartOutputDto:

        cart = self.cart_repository.find_cart(user_id=input.user_id)

        return FindCartOutputDto(id=cart.id, user_id=cart.user_id, items=cart.items, total_price=cart.total_price)