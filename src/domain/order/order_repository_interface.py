from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.order.order_entity import Order


class OrderRepositoryInterface(ABC):

    @abstractmethod
    async def create_order(self, order: Order) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def find_order(self, order_id: UUID, user_id: UUID) -> Order:
        raise NotImplementedError
    
    @abstractmethod
    async def find_order_by_cart_id(self, cart_id: UUID) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def update_order(self, order: Order) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def list_orders(self, user_id: UUID) -> List[Order]:
        raise NotImplementedError
    
    @abstractmethod
    async def list_all_orders(self) -> List[Order]:
        raise NotImplementedError
    
    @abstractmethod
    async def remove_order(self, order_id: UUID) -> UUID:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_orders(self) -> None:
        raise NotImplementedError