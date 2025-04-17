import uuid
from uuid import UUID

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.cart_item.cart_item_entity import CartItem
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from usecases.cart_item.add_item.add_item_dto import (AddItemInputDto,
                                                      AddItemOutputDto)
from usecases.cart_item.update_item.update_item_dto import UpdateItemInputDto
from usecases.cart_item.update_item.update_item_usecase import \
    UpdateItemUseCase


class AddItemUseCase(UseCaseInterface):
    def __init__(self, cart_item_repository: CartItemRepositoryInterface, product_repository: ProductRepositoryInterface):
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    def execute(self, user_id: UUID, cart_id: UUID, input: AddItemInputDto) -> AddItemOutputDto:
    
        # verificar se o produto existe
        product_found = self.product_repository.find_product(product_id=input.product_id)

        if product_found is None:
            raise ValueError(f"Product with code '{input.product_id}' not found")

        # verificar se o produto esta no carrinho
        find_item = self.cart_item_repository.find_item(item_id=product_found.id)
        
        if find_item:
            usecase = UpdateItemUseCase(cart_item_repository=self.cart_item_repository)
            find_item.quantity += input.quantity
            output = usecase.execute(cart_item_id=find_item.id, input=UpdateItemInputDto(quantity=find_item.quantity))
            return AddItemOutputDto(id=output.id, user_id=user_id, cart_id=output.cart_id,product_id=output.product_id, quantity=output.quantity)

        cart_item = CartItem(id=uuid.uuid4(), cart_id=cart_id, product_id=input.product_id, quantity=input.quantity)

        self.cart_item_repository.add_item(cart_item=cart_item)

        return AddItemOutputDto(id=cart_item.id, user_id=user_id, cart_id=cart_item.cart_id, product_id=cart_item.product_id, quantity=cart_item.quantity)