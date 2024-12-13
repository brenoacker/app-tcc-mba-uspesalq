import uuid
from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.product.product_entity import Product
from src.domain.product.product_repository_interface import ProductRepositoryInterface
from src.usecases.product.add_product.add_product_dto import AddProductInputDto, AddProductOutputDto


class AddProductUseCase(UseCaseInterface):
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self, input: AddProductInputDto) -> AddProductOutputDto:
        
        product = Product(id=uuid.uuid4(), name=input.name, price=input.price, category=input.category)

        self.product_repository.add_product(product=product)

        return AddProductOutputDto(id=product.id, name=product.name, price=product.price, category=product.category)