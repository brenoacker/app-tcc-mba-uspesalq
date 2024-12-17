import uuid

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_repository_interface import CartRepositoryInterface
from domain.cart_item.cart_item_entity import CartItem
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from usecases.cart_item.add_item.add_item_dto import (AddItemInputDto,
                                                      AddItemOutputDto)


class AddItemUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface):
        self.cart_item_repository = cart_item_repository

    def execute(self, input: AddItemInputDto) -> AddItemOutputDto:
        cart_item = CartItem(id=uuid.uuid4(), user_id=input.user_id, product_id=input.product_id, quantity=input.quantity)

        self.cart_item_repository.add_item(cart=cart_item)

        return AddItemOutputDto(id=cart_item.id, user_id=cart_item.user_id, product_id=cart_item.product_id, quantity=cart_item.quantity)