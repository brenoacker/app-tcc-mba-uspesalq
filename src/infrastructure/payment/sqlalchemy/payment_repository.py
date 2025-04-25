import asyncio
from typing import List
from uuid import UUID

import psycopg2
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.payment.payment_entity import Payment
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from infrastructure.payment.sqlalchemy.payment_model import PaymentModel


class PaymentRepository(PaymentRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, payment: Payment) -> Payment:
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                payment_model = PaymentModel(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status)
                self.session.add(payment_model)
                await self.session.commit()
                # Evitando a chamada para refresh que causa uma consulta adicional ao banco
                return payment
            except psycopg2.errors.DeadlockDetected:
                await self.session.rollback()
                retries += 1
                # Reduzindo o tempo de espera para melhorar throughput
                await asyncio.sleep(0.1 * retries)  # Linear backoff com tempo menor
            except Exception as e:
                await self.session.rollback()
                raise e
        raise Exception("Max retries exceeded for create_payment")

    async def execute_payment(self, payment: Payment) -> Payment:
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                query = update(PaymentModel).where(PaymentModel.id == payment.id).values(
                    payment_method=payment.payment_method,
                    payment_card_gateway=payment.payment_card_gateway,
                    status=payment.status
                )
                await self.session.execute(query)
                await self.session.commit()
                # Já temos todas as informações do payment, não precisamos consultar novamente
                return payment
            
            except psycopg2.errors.DeadlockDetected:
                await self.session.rollback()
                retries += 1
                # Reduzindo o tempo de espera para melhorar throughput
                await asyncio.sleep(0.1 * retries)  # Linear backoff com tempo menor
            except Exception as e:
                await self.session.rollback()
                raise e
        raise Exception("Max retries exceeded for execute_payment")
                

    async def find_payment(self, payment_id: UUID) -> Payment:
        result = await self.session.execute(
            select(PaymentModel).filter(PaymentModel.id == payment_id)
        )
        payment_found = result.scalars().first()

        if payment_found is None:
            return None
        
        return Payment(id=payment_found.id, user_id=payment_found.user_id, order_id=payment_found.order_id, payment_method=payment_found.payment_method, payment_card_gateway=payment_found.payment_card_gateway, status=payment_found.status)	

    async def list_payments(self, user_id: UUID) -> List[Payment]:
        result = await self.session.execute(
            select(PaymentModel).filter(PaymentModel.user_id == user_id)
        )
        payments_found = result.scalars().all()

        if not payments_found:
            return []
        
        return [Payment(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status) for payment in payments_found]
    
    async def list_all_payments(self) -> List[Payment]:
        result = await self.session.execute(select(PaymentModel))
        payments_found = result.scalars().all()

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
        
    async def delete_all_payments(self) -> None:
        await self.session.execute(
            PaymentModel.__table__.delete()
        )
        await self.session.commit()
        
    
    async def find_payment_by_order_id(self, order_id: UUID) -> Payment:
        result = await self.session.execute(
            select(PaymentModel).filter(PaymentModel.order_id == order_id)
        )
        payment_found = result.scalars().first()

        if payment_found is None:
            return None
        
        return Payment(id=payment_found.id, user_id=payment_found.user_id, order_id=payment_found.order_id, payment_method=payment_found.payment_method, payment_card_gateway=payment_found.payment_card_gateway, status=payment_found.status)