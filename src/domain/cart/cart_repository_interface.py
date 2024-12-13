from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from src.domain.cart.cart_entity import Cart


class CartRepositoryInterface(ABC):

    @abstractmethod
    def add_cart(self, item: Cart) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_cart(self, item: Cart) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_cart(self, item_id: UUID) -> None:
        raise NotImplementedError

