import logging

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from usecases.product.list_products.list_products_dto import (
    ListProductsDto, ListProductsInputDto, ListProductsOutputDto)


class ListProductsUseCase(UseCaseInterface):
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    async def execute(self) -> ListProductsOutputDto:

        products = await self.product_repository.list_products()

        if products is None:
            return ListProductsOutputDto(products=[])

        products_list = [ListProductsDto(id=product.id, name=product.name, price=product.price, category=product.category) for product in products]

        return ListProductsOutputDto(products=products_list)