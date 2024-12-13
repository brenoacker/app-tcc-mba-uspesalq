from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from src.domain.payment.payment_entity import Payment


class PaymentRepositoryInterface(ABC):

    @abstractmethod
    def create_payment(self, payment: Payment) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_payment(self, payment_id: UUID) -> Payment:
        raise NotImplementedError

    @abstractmethod
    def update_payment(self, payment: Payment) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_payments(self, user_id: UUID = None, start_date: str = None, end_date: str = None) -> List[Payment]:
        raise NotImplementedError

    @abstractmethod
    def cancel_payment(self, payment_id: UUID) -> None:
        raise NotImplementedError
