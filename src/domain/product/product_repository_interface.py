from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.product.product_entity import Product


class ProductRepositoryInterface(ABC):

    @abstractmethod
    def add_product(self, product: Product) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_product(self, product_id: UUID) -> Product:
        raise NotImplementedError

    @abstractmethod
    def update_product(self, product: Product) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_products(self) -> List[Product]:
        raise NotImplementedError