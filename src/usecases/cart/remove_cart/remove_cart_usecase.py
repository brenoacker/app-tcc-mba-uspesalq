from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_repository_interface import CartRepositoryInterface
from usecases.cart.remove_cart.remove_cart_dto import (RemoveCartInputDto,
                                                       RemoveCartOutputDto)


class RemoveCartUseCase(UseCaseInterface):
    def __init__(self, cart_repository: CartRepositoryInterface):
        self.cart_repository = cart_repository

    def execute(self, input: RemoveCartInputDto) -> RemoveCartOutputDto:

        self.cart_repository.remove_cart(cart_id=input.id)
        
        return RemoveCartOutputDto(id=input.id, user_id=input.user_id)