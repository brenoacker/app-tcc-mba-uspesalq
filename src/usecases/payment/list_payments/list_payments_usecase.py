from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from usecases.payment.list_payments.list_payments_dto import (
    ListPaymentsDto, ListPaymentsInputDto, ListPaymentsOutputDto)


class ListPaymentsUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    async def execute(self, input: ListPaymentsInputDto) -> ListPaymentsOutputDto:
        
        payments = await self.payment_repository.list_payments(user_id=input.user_id)

        if payments is None:
            return ListPaymentsOutputDto(payments=[])

        list_payments = [ListPaymentsDto(id=payment.id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status) for payment in payments]
        
        return ListPaymentsOutputDto(payments=list_payments)