import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.api.database import get_session
from infrastructure.cart.sqlalchemy.cart_repository import CartRepository
from infrastructure.order.sqlalchemy.order_repository import OrderRepository
from infrastructure.payment.sqlalchemy.payment_repository import \
    PaymentRepository
from usecases.cart.delete_all_carts.delete_all_carts_usecase import \
    DeleteAllCartsUseCase
from usecases.order.delete_all_orders.delete_all_orders_usecase import \
    DeleteAllOrdersUseCase
from usecases.payment.delete_all_payments.delete_all_payments_usecase import \
    DeleteAllPaymentsUseCase

router = APIRouter(prefix="/db", tags=["DB"])

@router.delete("/delete_carts_orders_and_payments", status_code=204)
def delete_carts_orders_and_payments(session: Session = Depends(get_session)):
    try:
        cart_repository = CartRepository(session=session)
        order_repository = OrderRepository(session=session)
        payment_repository = PaymentRepository(session=session)
        usecase = DeleteAllPaymentsUseCase(payment_repository=payment_repository)
        usecase.execute()
        usecase = DeleteAllOrdersUseCase(order_repository=order_repository)
        usecase.execute()
        usecase = DeleteAllCartsUseCase(cart_repository=cart_repository)
        usecase.execute()
        return {"message": "All carts, orders and payments deleted"}   
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e