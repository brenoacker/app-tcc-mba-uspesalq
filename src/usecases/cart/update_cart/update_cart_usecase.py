import uuid
from typing import Optional
from uuid import UUID

from fastapi.responses import JSONResponse

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_entity import Cart
from domain.cart.cart_repository_interface import CartRepositoryInterface
from domain.cart_item.cart_item_entity import CartItem
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from usecases.cart.update_cart.update_cart_dto import (UpdateCartInputDto,
                                                       UpdateCartOutputDto)
from usecases.product.find_product.find_product_validation import \
    FindProductValidation


class UpdateCartUseCase(UseCaseInterface):
    def __init__(self, cart_repository: CartRepositoryInterface, cart_item_repository: CartItemRepositoryInterface, product_repository: ProductRepositoryInterface):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    async def execute(self, user_id: UUID, cart_id: UUID, input: UpdateCartInputDto) -> UpdateCartOutputDto:
        
        # validando se o cart existe
        cart_found = await self.cart_repository.find_cart(cart_id=cart_id, user_id=user_id)

        if not cart_found:
            raise ValueError("Cart not found")
        
        cart_items_found = await self.cart_item_repository.find_items_by_cart_id(cart_id=cart_id)

        if not cart_items_found:
            raise ValueError("Cart items not found for this cart")


        # validando se os produtos enviados existem
        find_product_validation = FindProductValidation(product_repository=self.product_repository)
        for item in input.items:
            product_exists = await find_product_validation.validate_product_exists(product_id=item.product_id)
            if not product_exists:
                raise ValueError(f"Product with code '{item.product_id}' not found")

        new_cart_items = []
        for item in input.items:
            cart_item = next((cart_item for cart_item in cart_items_found if cart_item.product_id == item.product_id), None)

            if cart_item:
                if item.quantity == 0:
                    await self.cart_item_repository.remove_item(item_id=cart_item.id)
                else:
                    cart_item.quantity = item.quantity
                    await self.cart_item_repository.update_item(item=cart_item)
            else:
                cart_item = CartItem(id=uuid.uuid4(), cart_id=cart_id, product_id=item.product_id, quantity=item.quantity)
                await self.cart_item_repository.add_item(cart_item=cart_item)
                new_cart_items.append(cart_item)

        cart_items_found_after_update = await self.cart_item_repository.find_items_by_cart_id(cart_id=cart_id)

        if not cart_items_found_after_update:
            await self.cart_repository.remove_cart(cart_id=cart_id)
            return JSONResponse(content={"message": "All items were removed from cart. Cart was removed."}, status_code=200)

        total_price = 0
        for cart_item in cart_items_found_after_update:
            product = await self.product_repository.find_product(product_id=cart_item.product_id)
            total_price += cart_item.quantity * product.price

        updated_cart = await self.cart_repository.update_cart(cart=Cart(id=cart_id, user_id=user_id, total_price=total_price))

        return UpdateCartOutputDto(id=updated_cart.id, user_id=updated_cart.user_id, total_price=updated_cart.total_price)