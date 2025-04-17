from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_repository_interface import CartRepositoryInterface


class DeleteAllCartsUseCase(UseCaseInterface):
    def __init__(self, cart_repository: CartRepositoryInterface):
        self.cart_repository = cart_repository

    def execute(self) -> None:
        self.cart_repository.delete_all_carts()
        
        return None