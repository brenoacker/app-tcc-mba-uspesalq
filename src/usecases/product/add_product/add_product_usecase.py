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
        
        find_product_by_name = self.product_repository.find_product_by_name(name=input.name)
        
        if find_product_by_name:
            raise ValueError(f"Product with '{input.name}' name already registered")

        find_product_by_id = self.product_repository.find_product(product_id=input.id)

        if find_product_by_id:
            raise ValueError(f"Product id '{input.id}' already registered")

        category = ProductCategory(input.category)

        product = Product(id=input.id, name=input.name, price=input.price, category=category)

        product_model = self.product_repository.add_product(product=product)

        return AddProductOutputDto(id=product_model.id, name=product_model.name, price=product_model.price, category=category)