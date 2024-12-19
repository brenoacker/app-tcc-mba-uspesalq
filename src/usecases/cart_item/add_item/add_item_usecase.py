import uuid
from uuid import UUID

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart.cart_repository_interface import CartRepositoryInterface
from domain.cart_item.cart_item_entity import CartItem
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.cart_item.add_item.add_item_dto import (AddItemInputDto,
                                                      AddItemOutputDto)
from usecases.cart_item.update_item.update_item_dto import UpdateItemInputDto
from usecases.cart_item.update_item.update_item_usecase import \
    UpdateItemUseCase
from usecases.user.find_user.find_user_dto import FindUserInputDto
from usecases.user.find_user.find_user_usecase import FindUserUseCase


class AddItemUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface, product_repository: ProductRepositoryInterface):
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    def execute(self, cart_id: UUID, input: AddItemInputDto) -> AddItemOutputDto:
    
        # verificar se o produto existe
        product_found = self.product_repository.find_product_by_code(product_code=input.product_code)

        if not product_found:
            raise ValueError(f"Product with code '{input.product_code}' not found")

        # verificar se o produto esta no carrinho
        find_item = self.cart_item_repository.find_item(item_id=product_found.id)
        
        if find_item:
            usecase = UpdateItemUseCase(cart_item_repository=self.cart_item_repository)
            find_item.quantity += input.quantity
            output = usecase.execute(input=UpdateItemInputDto(quantity=find_item.quantity))
            return AddItemOutputDto(id=output.id, user_id=output.user_id, cart_id=output.cart_id,product_code=output.product_code, quantity=output.quantity)

        cart_item = CartItem(id=uuid.uuid4(), user_id=user_id, cart_id=cart_id, product_code=input.product_code, quantity=input.quantity)

        self.cart_item_repository.add_item(cart_item=cart_item)

        return AddItemOutputDto(id=cart_item.id, user_id=cart_item.user_id, cart_id=cart_item.cart_id, product_code=cart_item.product_code, quantity=cart_item.quantity)