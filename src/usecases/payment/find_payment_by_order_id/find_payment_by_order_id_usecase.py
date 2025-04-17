from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.payment.payment_entity import Payment
from domain.user.user_repository_interface import UserRepositoryInterface
from infrastructure.payment.sqlalchemy.payment_repository import \
    PaymentRepository
from usecases.payment.find_payment_by_order_id.find_payment_by_order_id_dto import (
    FindPaymentByOrderIdInputDto, FindPaymentByOrderIdOutputDto)


class FindPaymentByOrderIdUsecase(UseCaseInterface):
    def __init__(self, payment_repository: PaymentRepository, user_repository: UserRepositoryInterface):
        self.payment_repository = payment_repository
        self.user_repository = user_repository

    def execute(self, input: FindPaymentByOrderIdInputDto) -> FindPaymentByOrderIdOutputDto:
        
        user = self.user_repository.find_user(user_id=input.user_id)

        if user is None:
            raise ValueError(f"User with id {input.user_id} not found")
        
        payment = self.payment_repository.find_payment_by_order_id(order_id=input.order_id)

        if payment is None:
            raise ValueError(f"Payment for order with id {input.order_id} not found")
        
        return FindPaymentByOrderIdOutputDto(id=payment.id, user_id=payment.user_id, order_id=payment.order_id, payment_method=payment.payment_method, payment_card_gateway=payment.payment_card_gateway, status=payment.status)