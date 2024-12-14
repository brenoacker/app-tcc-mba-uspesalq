from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.product.product_repository_interface import ProductRepositoryInterface
from src.usecases.product.list_products.list_products_dto import ListProductsInputDto, ListProductsOutputDto


class ListProductsUseCase(UseCaseInterface):
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self, input: ListProductsInputDto) -> ListProductsOutputDto:

        products = self.product_repository.list_products()

        return ListProductsOutputDto(products=products)