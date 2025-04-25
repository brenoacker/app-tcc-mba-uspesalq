from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from usecases.product.update_product.update_product_dto import (
    UpdateProductInputDto, UpdateProductOutputDto)


class UpdateProductUseCase(UseCaseInterface):
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    async def execute(self, input: UpdateProductInputDto) -> UpdateProductOutputDto:
        
        product = await self.product_repository.find_product(product_id=input.id)

        if not product:
            raise ValueError(f"Product with id '{input.id}' not found")

        product.id = input.id
        product.name = input.name
        product.price = input.price
        product.category = input.category

        await self.product_repository.update_product(product=product)

        return UpdateProductOutputDto(id=product.id, name=product.name, price=product.price, category=product.category)