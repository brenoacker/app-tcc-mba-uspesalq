import logging

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from usecases.product.list_products.list_products_dto import (
    ListProductsDto, ListProductsInputDto, ListProductsOutputDto)


class ListProductsUseCase(UseCaseInterface):
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self) -> ListProductsOutputDto:

        products = self.product_repository.list_products()

        # for product in products:
        #     logging.info(f'ListProductsUseCase - product: {product.id} - {product.name} - {product.price} - {product.category}')

        return ListProductsOutputDto(products=products)