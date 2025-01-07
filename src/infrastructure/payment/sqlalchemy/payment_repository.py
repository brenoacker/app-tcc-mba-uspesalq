
import time
from typing import List
from uuid import UUID

import psycopg2
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.session import Session

from domain.payment.payment_entity import Payment
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from infrastructure.payment.sqlalchemy.payment_model import PaymentModel


class PaymentRepository(PaymentRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create_payment(self, payment: Payment) -> Payment:
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                self.session.add(PaymentModel(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status))
                self.session.commit()
                return Payment(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status)
            except psycopg2.errors.DeadlockDetected:
                self.session.rollback()
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff
            except OperationalError as e:
                self.session.rollback()
                raise e
        raise Exception("Max retries exceeded for create_payment")

    def execute_payment(self, payment: Payment) -> Payment:
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                self.session.query(PaymentModel).filter(PaymentModel.id == payment.id).update(
                    {
                        "payment_method": payment.payment_method,
                        "payment_card_gateway": payment.payment_card_gateway,
                        "status": payment.status
                    }
                )
                self.session.commit()

                return Payment(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status)
            
            except psycopg2.errors.DeadlockDetected:
                self.session.rollback()
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff
            except OperationalError as e:
                self.session.rollback()
                raise e
            except Exception as e:
                self.session.rollback()
                raise e
        raise Exception("Max retries exceeded for execute_payment")

    def find_payment(self, payment_id: UUID) -> Payment:
        
        payment_found = self.session.query(PaymentModel).filter(PaymentModel.id == payment_id).first()

        if payment_found is None:
            return None
        
        return Payment(id=payment_found.id, user_id=payment_found.user_id, order_id=payment_found.order_id, payment_method=payment_found.payment_method, payment_card_gateway=payment_found.payment_card_gateway, status=payment_found.status)	

    def find_payment_by_order_id(self, order_id: UUID) -> Payment:
        
        payment_found = self.session.query(PaymentModel).filter(PaymentModel.order_id == order_id).first()

        if payment_found is None:
            return None
        
        return Payment(id=payment_found.id, user_id=payment_found.user_id, order_id=payment_found.order_id, payment_method=payment_found.payment_method, payment_card_gateway=payment_found.payment_card_gateway, status=payment_found.status)

    def list_payments(self, user_id: UUID) -> List[Payment]:
        
        payments_found: List[PaymentModel] = self.session.query(PaymentModel).filter(PaymentModel.user_id == user_id).all()

        if not payments_found:
            return []
        
        return [Payment(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status) for payment in payments_found]
    
    def list_all_payments(self) -> List[Payment]:
        
        payments_found: List[PaymentModel] = self.session.query(PaymentModel).all()

        if not payments_found:
            return []
        
        return [Payment(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status) for payment in payments_found]
    
    def delete_all_payments(self) -> None:
        self.session.query(PaymentModel).delete()
        self.session.commit()

        return None