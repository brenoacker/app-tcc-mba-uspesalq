from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.cart_item.cart_item_entity import CartItem


class CartItemRepositoryInterface(ABC):

    @abstractmethod
    async def add_item(self, cart_item: CartItem) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_item(self, item_id: UUID) -> Optional[CartItem]:
        raise NotImplementedError
    
    @abstractmethod
    async def find_items_by_cart_id(self, cart_id: UUID) -> Optional[List[CartItem]]:
        raise NotImplementedError

    @abstractmethod
    async def update_item(self, item: CartItem) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_item(self, item_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_items(self) -> Optional[List[CartItem]]:
        raise NotImplementedError
    
    @abstractmethod
    async def list_items_by_user(self, user_id: UUID) -> Optional[List[CartItem]]:
        raise NotImplementedError
