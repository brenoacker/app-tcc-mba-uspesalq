from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.cart.cart_entity import Cart


class CartRepositoryInterface(ABC):

    @abstractmethod
    async def add_cart(self, cart: Cart) -> Cart:
        raise NotImplementedError
    
    @abstractmethod
    async def find_cart(self, cart_id: UUID, user_id: UUID) -> Cart:
        raise NotImplementedError

    @abstractmethod
    async def update_cart(self, cart: Cart) -> Cart:
        raise NotImplementedError

    @abstractmethod
    async def remove_cart(self, cart_id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def list_carts(self, user_id: UUID) -> List[Cart]:
        raise NotImplementedError

    @abstractmethod
    async def delete_all_carts(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete_all_carts(self) -> None:
        raise NotImplementedError

