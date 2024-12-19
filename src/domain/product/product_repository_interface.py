from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.product.product_entity import Product


class ProductRepositoryInterface(ABC):

    @abstractmethod
    def add_product(self, product: Product) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_product(self, product_id: int) -> Optional[Product]:
        raise NotImplementedError
    
    @abstractmethod
    def find_product_by_name(self, name: str) -> Product:
        raise NotImplementedError
    
    @abstractmethod
    def update_product(self, product: Product) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_products(self) -> List[Product]:
        raise NotImplementedError
    
    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        raise NotImplementedError