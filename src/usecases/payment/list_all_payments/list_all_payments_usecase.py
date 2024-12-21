from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from usecases.payment.list_all_payments.list_all_payments_dto import (
    ListAllPaymentsDto, ListAllPaymentsOutputDto)


class ListAllPaymentsUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    def execute(self) -> ListAllPaymentsOutputDto:
        payments = self.payment_repository.list_all_payments()

        if payments is None:
            return ListAllPaymentsOutputDto(payments=[])
        
        return ListAllPaymentsOutputDto(payments=[ListAllPaymentsDto(id=payment.id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway) for payment in payments])