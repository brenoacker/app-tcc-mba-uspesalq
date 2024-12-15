from datetime import datetime
import uuid
from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.payment.payment_entity import Payment
from src.domain.payment.payment_method_enum import PaymentMethod
from src.domain.payment.payment_repository_interface import PaymentRepositoryInterface
from src.domain.payment.payment_status_enum import PaymentStatus
from src.usecases.payment.execute_payment.execute_payment_dto import ExecutePaymentInputDto, ExecutePaymentOutputDto


class ExecutePaymentUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    def execute(self, input: ExecutePaymentInputDto) -> ExecutePaymentOutputDto:

        payment = Payment(
            id=uuid.uuid4(), 
            order_id=input.order_id, 
            amount=input.amount, 
            payment_method=input.payment_method, 
            status=PaymentStatus.INITIATED,
            payment_card_gateway=input.payment_card_gateway, 
            created_at=datetime.now(), 
            updated_at=datetime.now()
        )

        executed_payment = self.payment_repository.execute_payment(payment=payment)

        return ExecutePaymentOutputDto(
            id=executed_payment.id, 
            order_id=executed_payment.order_id, 
            amount=executed_payment.amount, 
            payment_method=executed_payment.payment_method, 
            payment_card_gateway=executed_payment.payment_card_gateway,
            status=executed_payment.status,
            created_at=executed_payment.created_at,
            updated_at=executed_payment.updated_at
        )
