from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.product.product_repository_interface import ProductRepositoryInterface
from src.usecases.product.find_product.find_product_dto import FindProductInputDto, FindProductOutputDto


class FindProductUsecase(UseCaseInterface):
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self, input: FindProductInputDto) -> FindProductOutputDto:
        
        product = self.product_repository.find_product(product_id=input.id)
        
        return FindProductOutputDto(id=product.id, name=product.name, price=product.price, category=product.category)