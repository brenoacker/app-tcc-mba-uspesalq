from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from src.domain.payment.payment_entity import Payment


class PaymentRepositoryInterface(ABC):

    @abstractmethod
    def execute_payment(self, payment: Payment) -> Payment:
        raise NotImplementedError
    
    @abstractmethod
    def list_payments(self, user_id: UUID) -> List[Payment]:
        raise NotImplementedError
