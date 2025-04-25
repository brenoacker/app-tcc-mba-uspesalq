import uuid

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_entity import Cart
from domain.cart.cart_repository_interface import CartRepositoryInterface
from domain.cart_item.cart_item_entity import CartItem
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from domain.product.product_entity import Product
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.cart.add_cart.add_cart_dto import (AddCartInputDto,
                                                 AddCartOutputDto)


class AddCartUseCase(UseCaseInterface):

    def __init__(self, cart_repository: CartRepositoryInterface, cart_item_repository: CartItemRepositoryInterface, user_repository: UserRepositoryInterface, product_repository: ProductRepositoryInterface):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.user_repository = user_repository
        self.product_repository = product_repository

    async def execute(self, user_id: uuid.UUID, input: AddCartInputDto) -> AddCartOutputDto:

        # validating if user exists
        user_found = await self.user_repository.find_user(user_id=user_id)

        if not user_found:
            raise ValueError(f"User with id '{user_id}' not found")
        
        total_price = 0

        class ProductAndQuantity():
            def __init__(self, product: Product, quantity: int):
                self.product = product
                self.quantity = quantity

        product_list = []

        # validating if all products exists
        for item in input.items:
            product_found = await self.product_repository.find_product(product_id=item.product_id)

            if not product_found:
                raise ValueError(f"Product with code '{item.product_id}' not found")
            
            total_price += product_found.price * item.quantity
            product_list.append(ProductAndQuantity(product=product_found, quantity=item.quantity))


        # creating cart
        cart_id = uuid.uuid4()

        cart = Cart(id=cart_id, user_id=user_id, total_price=total_price)

        await self.cart_repository.add_cart(cart=cart)

        # adding items to cart
        for product in product_list:
            await self.cart_item_repository.add_item(cart_item=CartItem(id=uuid.uuid4(), cart_id=cart_id, product_id=product.product.id, quantity=product.quantity))
        
        return AddCartOutputDto(id=cart.id, user_id=cart.user_id, total_price=cart.total_price)
    