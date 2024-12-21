from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from usecases.payment.list_payments.list_payments_dto import (
    ListPaymentsInputDto, ListPaymentsOutputDto)


class ListPaymentsUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    def execute(self, input: ListPaymentsInputDto) -> ListPaymentsOutputDto:
        
        payments = self.payment_repository.list_payments(user_id=input.user_id)

        if payments is None:
            return ListPaymentsOutputDto(payments=[])

        return ListPaymentsOutputDto(payments=payments)