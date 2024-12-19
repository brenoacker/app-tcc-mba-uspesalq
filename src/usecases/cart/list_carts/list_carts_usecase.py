from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_repository_interface import CartRepositoryInterface
from usecases.cart.list_carts.list_carts_dto import (ListCartsDto,
                                                     ListCartsInputDto,
                                                     ListCartsOutputDto)


class ListCartsUseCase(UseCaseInterface):
    def __init__(self, cart_repository: CartRepositoryInterface):
        self.cart_repository = cart_repository

    def execute(self, input: ListCartsInputDto) -> ListCartsOutputDto:

        list_carts_found = self.cart_repository.list_carts(user_id=input.user_id)

        if not list_carts_found:
            raise ValueError("No carts found")
        
        list_carts_dto = [ListCartsDto(id=cart.id, user_id=cart.user_id, total_price=cart.total_price) for cart in list_carts_found]
        
        return ListCartsOutputDto(carts=list_carts_dto)