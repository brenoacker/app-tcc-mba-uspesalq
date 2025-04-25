from infrastructure.product.sqlalchemy.product_repository import \
    ProductRepository


class FindProductValidation:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def validate_product_exists(self, product_id: int) -> bool:
        product_found = await self.product_repository.find_product(product_id=product_id)

        if not product_found:
            return False
        else:
            return True