from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from src.domain.cart.cart_entity import Cart


class CartRepositoryInterface(ABC):

    @abstractmethod
    def add_cart(self, cart: Cart) -> Cart:
        raise NotImplementedError
    
    @abstractmethod
    def find_cart(self, user_id: UUID) -> Cart:
        raise NotImplementedError

    @abstractmethod
    def update_cart(self, cart: Cart) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_cart(self, cart_id: UUID) -> None:
        raise NotImplementedError

