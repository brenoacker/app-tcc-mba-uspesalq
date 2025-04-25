from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.payment.payment_repository_interface import \
    PaymentRepositoryInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.payment.find_payment.find_payment_dto import (
    FindPaymentInputDto, FindPaymentOutputDto)


class FindPaymentUseCase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepositoryInterface, user_repository: UserRepositoryInterface):
        self.payment_repository = payment_repository
        self.user_repository = user_repository

    async def execute(self, input: FindPaymentInputDto) -> FindPaymentOutputDto:

        user = await self.user_repository.find_user(user_id=input.user_id)

        if user is None:
            raise ValueError(f"User with id {input.user_id} not found")

        payment = await self.payment_repository.find_payment(payment_id=input.id)

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
    