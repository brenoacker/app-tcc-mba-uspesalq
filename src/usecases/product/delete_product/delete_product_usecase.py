from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from usecases.product.delete_product.delete_product_dto import (
    DeleteProductInputDto, DeleteProductOutputDto)


class DeleteProductUseCase(UseCaseInterface):
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    async def execute(self, input: DeleteProductInputDto) -> DeleteProductOutputDto:
        await self.product_repository.delete_product(product_id=input.id)
        return DeleteProductOutputDto(id=input.id)