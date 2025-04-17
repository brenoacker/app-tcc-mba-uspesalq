from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface


class DeleteAllPaymentsUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    async def execute(self, input=None) -> None:
        await self.payment_repository.delete_all_payments()
        return None 