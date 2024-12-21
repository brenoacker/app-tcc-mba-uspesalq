from uuid import UUID

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.payment.payment_entity import Payment
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from usecases.payment.find_payment.find_payment_dto import (
    FindPaymentInputDto, FindPaymentOutputDto)


class FindPaymentUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    def execute(self, input: FindPaymentInputDto) -> FindPaymentOutputDto:
        payment = self.payment_repository.find_payment(payment_id=input.id, user_id=input.user_id)

        if payment is None:
            raise ValueError(f"Payment with id {input.id} not found")

        return FindPaymentOutputDto(
            id=payment.id, 
            user_id=payment.user_id, 
            order_id=payment.order_id, 
            payment_method=payment.payment_method, 
            payment_card_gateway=payment.payment_card_gateway,
            status=payment.status
        )
    