from domain.__seedwork.use_case_interface import UseCaseInterface
from infrastructure.cart.sqlalchemy.cart_repository import CartRepository
from infrastructure.cart_item.sqlalchemy.cart_item_repository import \
    CartItemRepository
from usecases.cart.find_cart_items.find_cart_items_dto import (
    FindCartItemDto, FindCartItemsInputDto, FindCartItemsOutputDto)


class FindCartItemsUseCase(UseCaseInterface):
    def __init__(self, cart_repository: CartRepository, cart_item_repository: CartItemRepository):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository

    def execute(self, input: FindCartItemsInputDto) -> FindCartItemsOutputDto:
        
        cart = self.cart_repository.find_cart(cart_id=input.cart_id, user_id=input.user_id)
        if cart is None:
            raise ValueError(f"Cart not found: {input.cart_id}")
        
        cart_items = self.cart_item_repository.find_items_by_cart_id(cart_id=input.cart_id)
        cart_items_dto = [FindCartItemDto(id=cart_item.id, product_id=cart_item.product_id, quantity=cart_item.quantity) for cart_item in cart_items]
        return FindCartItemsOutputDto(items=cart_items_dto)