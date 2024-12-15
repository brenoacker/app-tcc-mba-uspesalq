from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.order_item.order_item_entity import OrderItem


class OrderItemRepositoryInterface(ABC):
    
    @abstractmethod
    def add_order_item(self, order_item: OrderItem) -> OrderItem:
        raise NotImplementedError

    @abstractmethod
    def find_order_item(self, order_item_id: UUID) -> OrderItem:
        raise NotImplementedError

    @abstractmethod
    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        raise NotImplementedError
    
    @abstractmethod
    def remove_order_item(self, order_item_id: UUID) -> None:
        raise NotImplementedError