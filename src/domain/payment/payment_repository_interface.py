from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.payment.payment_entity import Payment


class PaymentRepositoryInterface(ABC):

    @abstractmethod
    def create_payment(self, payment: Payment) -> Payment:
        raise NotImplementedError

    @abstractmethod
    def execute_payment(self, payment: Payment) -> Payment:
        raise NotImplementedError
    
    @abstractmethod
    def list_payments(self, user_id: UUID) -> List[Payment]:
        raise NotImplementedError

    @abstractmethod
    def list_all_payments(self) -> List[Payment]:
        raise NotImplementedError

    @abstractmethod
    def find_payment(self, payment_id: UUID) -> Payment:
        raise NotImplementedError
    
    @abstractmethod
    def find_payment_by_order_id(self, order_id: UUID) -> Payment:
        raise NotImplementedError
    
    @abstractmethod
    def delete_all_payments(self) -> None:
        raise NotImplementedError