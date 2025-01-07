from domain.product.product_repository_interface import \
    ProductRepositoryInterface


class DeleteAllProductsUseCase:
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self) -> None:

        self.product_repository.delete_all_products()

        return None