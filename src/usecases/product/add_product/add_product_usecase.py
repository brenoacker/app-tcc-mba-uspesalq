
import uuid

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from usecases.product.add_product.add_product_dto import (AddProductInputDto,
                                                          AddProductOutputDto)


class AddProductUseCase(UseCaseInterface):
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self, input: AddProductInputDto) -> AddProductOutputDto:
        
        category = ProductCategory(input.category)

        product = Product(id=uuid.uuid4(), name=input.name, price=input.price, category=category)

        product_model = self.product_repository.add_product(product=product)

        return AddProductOutputDto(id=product_model.id, product_code=product_model.product_code, name=product_model.name, price=product_model.price, category=category)