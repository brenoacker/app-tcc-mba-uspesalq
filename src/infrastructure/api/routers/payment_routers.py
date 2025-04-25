import time
import traceback
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.order.order_status_enum import OrderStatus
from domain.payment.payment_status_enum import PaymentStatus
from infrastructure.api.database import get_session
from infrastructure.messaging.producer import publish_message
from infrastructure.order.sqlalchemy.order_repository import OrderRepository
from infrastructure.payment.sqlalchemy.payment_repository import \
    PaymentRepository
from infrastructure.user.sqlalchemy.user_repository import UserRepository
from usecases.order.find_order.find_order_dto import FindOrderInputDto
from usecases.order.find_order.find_order_usecase import FindOrderUseCase
from usecases.order.update_order.update_order_dto import UpdateOrderInputDto
from usecases.order.update_order.update_order_usecase import UpdateOrderUseCase
from usecases.payment.execute_payment.execute_payment_dto import \
    ExecutePaymentInputDto
from usecases.payment.execute_payment.execute_payment_usecase import \
    ExecutePaymentUseCase
from usecases.payment.find_payment.find_payment_dto import FindPaymentInputDto
from usecases.payment.find_payment.find_payment_usecase import \
    FindPaymentUseCase
from usecases.payment.find_payment_by_order_id.find_payment_by_order_id_dto import \
    FindPaymentByOrderIdInputDto
from usecases.payment.find_payment_by_order_id.find_payment_by_order_id_usecase import \
    FindPaymentByOrderIdUsecase
from usecases.payment.list_all_payments.list_all_payments_usecase import \
    ListAllPaymentsUseCase
from usecases.payment.list_payments.list_payments_dto import \
    ListPaymentsInputDto
from usecases.payment.list_payments.list_payments_usecase import \
    ListPaymentsUseCase

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/{order_id}", status_code=201)
async def execute_payment(request: ExecutePaymentInputDto, order_id: UUID, user_id: UUID = Header(...), session: AsyncSession = Depends(get_session)):
    try:
        payment_repository = PaymentRepository(session=session)
        user_repository = UserRepository(session=session)
        order_repository = OrderRepository(session=session)
        usecase = ExecutePaymentUseCase(payment_repository=payment_repository, user_repository=user_repository, order_repository=order_repository)
        output = await usecase.execute(order_id=order_id, user_id=user_id, input=ExecutePaymentInputDto(payment_method=request.payment_method, payment_card_gateway=request.payment_card_gateway))
        return output
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
# def update_order_status_after_payment(order_id: UUID, user_id: UUID, status: OrderStatus):
#     # time.sleep(5)
#     response = requests.patch(url=f"http://localhost:8000/order/internal/{order_id}",json={"status": status.value}, headers={"user-id": str(user_id)})
#     if response.status_code != 200:
#         raise Exception(f"Error updating order status: {response.text}")

@router.get("/", status_code=200)
async def list_payments(user_id: UUID = Header(...), session: AsyncSession = Depends(get_session)):
    try:
        payment_repository = PaymentRepository(session=session)
        usecase = ListPaymentsUseCase(payment_repository=payment_repository)
        output = await usecase.execute(input=ListPaymentsInputDto(user_id=user_id))
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/id/{payment_id}", status_code=200)
async def find_payment(payment_id: UUID, user_id: UUID = Header(...), session: AsyncSession = Depends(get_session)):
    try:
        payment_repository = PaymentRepository(session=session)
        user_repository = UserRepository(session=session)
        usecase = FindPaymentUseCase(payment_repository=payment_repository, user_repository=user_repository)
        output = await usecase.execute(input=FindPaymentInputDto(id=payment_id, user_id=user_id))
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/order/{order_id}", status_code=200)
async def find_payment_by_order_id(order_id: UUID, user_id: UUID = Header(...), session: AsyncSession = Depends(get_session)):
    try:
        payment_repository = PaymentRepository(session=session)
        user_repository = UserRepository(session=session)
        usecase = FindPaymentByOrderIdUsecase(payment_repository=payment_repository, user_repository=user_repository)
        output = await usecase.execute(input=FindPaymentByOrderIdInputDto(order_id=order_id, user_id=user_id))
        return output
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e

@router.get("/all_payments", status_code=200)
async def list_all_payments(session: AsyncSession = Depends(get_session)):
    try:
        payment_repository = PaymentRepository(session=session)
        usecase = ListAllPaymentsUseCase(payment_repository=payment_repository)
        output = await usecase.execute()
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
# @router.delete("/", status_code=200)
# def delete_all_payments(session: Session = Depends(get_session)):
#     try:
#         payment_repository = PaymentRepository(session=session)
#         usecase = DeleteAllPaymentsUseCase(payment_repository=payment_repository)
#         usecase.execute()
#         return {"message": "All payments deleted"}
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
