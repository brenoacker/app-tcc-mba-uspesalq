from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.cart.cart_entity import Cart
from domain.cart_item.cart_item_entity import CartItem


class CartRepositoryInterface(ABC):

    @abstractmethod
    def add_cart(self, cart: Cart) -> Cart:
        raise NotImplementedError
    
    @abstractmethod
    def find_cart(self, cart_id: UUID, user_id: UUID) -> Cart:
        raise NotImplementedError

    @abstractmethod
    def update_cart(self, cart: Cart) -> Cart:
        raise NotImplementedError

    @abstractmethod
    def remove_cart(self, cart_id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def list_carts(self, user_id: UUID) -> List[Cart]:
        raise NotImplementedError

