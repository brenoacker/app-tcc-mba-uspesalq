from typing import List
from uuid import UUID

from sqlalchemy.orm.session import Session

from domain.payment.payment_entity import Payment
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from infrastructure.payment.sqlalchemy.payment_model import PaymentModel


class PaymentRepository(PaymentRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def execute_payment(self, payment: Payment) -> Payment:
        self.session.add(PaymentModel(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status))
        
        self.session.commit()

        return Payment(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status)

    def find_payment(self, payment_id: int, user_id: int) -> Payment:
        
        # talvez tenha que usar o _and
        payment_found = self.session.query(PaymentModel).filter(PaymentModel.id == payment_id, PaymentModel.user_id == user_id).first()

        if payment_found is None:
            return None
        
        return Payment(id=payment_found.id, user_id=payment_found.user_id, order_id=payment_found.order_id, payment_method=payment_found.payment_method, payment_card_gateway=payment_found.payment_card_gateway, status=payment_found.status)	

    def list_payments(self, user_id: UUID) -> List[Payment]:
        
        payments_found: List[PaymentModel] = self.session.query(PaymentModel).filter(PaymentModel.user_id == user_id).all()

        if not payments_found:
            return []
        
        return [
            {
                "id": payment.id,
                "user_id": payment.user_id,
                "order_id": payment.order_id,
                "payment_method": payment.payment_method,
                "payment_card_gateway": payment.payment_card_gateway,
                "status": payment.status
            }
            for payment in payments_found
        ]
    
    def list_all_payments(self) -> List[Payment]:
        
        payments_found: List[PaymentModel] = self.session.query(PaymentModel).all()

        if not payments_found:
            return []
        
        return [
            {
                "id": payment.id,
                "user_id": payment.user_id,
                "order_id": payment.order_id,
                "payment_method": payment.payment_method,
                "payment_card_gateway": payment.payment_card_gateway,
                "status": payment.status
            }
            for payment in payments_found
        ]