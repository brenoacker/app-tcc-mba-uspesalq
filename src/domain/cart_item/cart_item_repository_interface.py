from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.cart_item.cart_item_entity import CartItem


class CartItemRepositoryInterface(ABC):

    @abstractmethod
    def add_item(self, item: CartItem) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_item(self, item_id: UUID) -> CartItem:
        raise NotImplementedError

    @abstractmethod
    def update_item(self, item: CartItem) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_item(self, item_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_items(self, user_id: UUID) -> List[CartItem]:
        raise NotImplementedError
