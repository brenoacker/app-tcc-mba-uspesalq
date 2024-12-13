from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from src.domain.order.order_entity import Order

class OrderRepositoryInterface(ABC):

    @abstractmethod
    def add_order(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_order(self, order_id: UUID) -> Order:
        raise NotImplementedError

    @abstractmethod
    def update_order(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_orders(self) -> List[Order]:
        raise NotImplementedError
    
    @abstractmethod
    def remove_order(self, order_id: UUID) -> None:
        raise NotImplementedError