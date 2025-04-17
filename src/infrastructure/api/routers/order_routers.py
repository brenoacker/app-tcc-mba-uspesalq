import traceback
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from infrastructure.api.database import get_session
from infrastructure.cart.sqlalchemy.cart_repository import CartRepository
from infrastructure.offer.sqlalchemy.offer_repository import OfferRepository
from infrastructure.order.sqlalchemy.order_repository import OrderRepository
from infrastructure.payment.sqlalchemy.payment_repository import \
    PaymentRepository
from infrastructure.user.sqlalchemy.user_repository import UserRepository
from usecases.order.create_order.create_order_dto import CreateOrderInputDto
from usecases.order.create_order.create_order_usecase import CreateOrderUseCase
from usecases.order.find_order.find_order_dto import FindOrderInputDto
from usecases.order.find_order.find_order_usecase import FindOrderUseCase
from usecases.order.list_all_orders.list_all_orders_usecase import \
    ListAllOrdersUseCase
from usecases.order.list_orders.list_orders_dto import ListOrdersInputDto
from usecases.order.list_orders.list_orders_usecase import ListOrdersUseCase
from usecases.order.update_order.update_order_dto import UpdateOrderInputDto
from usecases.order.update_order.update_order_usecase import UpdateOrderUseCase

router = APIRouter(prefix="/order", tags=["Order"])

@router.post("/", status_code=201)
def create_order(request: CreateOrderInputDto, user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        order_repository = OrderRepository(session=session)
        user_repository = UserRepository(session=session)
        cart_repository = CartRepository(session=session)
        offer_repository = OfferRepository(session=session)
        payment_repository = PaymentRepository(session=session)
        usecase = CreateOrderUseCase(order_repository=order_repository, user_repository=user_repository, cart_repository=cart_repository, offer_repository=offer_repository, payment_repository=payment_repository)
        if not request.offer_id:
            request.offer_id = None
        output = usecase.execute(user_id = user_id, input=CreateOrderInputDto(type=request.type,cart_id=request.cart_id, offer_id=request.offer_id))
        return output
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/", status_code=200)
def list_orders(user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        order_repository = OrderRepository(session=session)
        usecase = ListOrdersUseCase(order_repository=order_repository)
        output = usecase.execute(input=ListOrdersInputDto(user_id=user_id))
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/all_orders", status_code=200)
def list_all_orders(session: Session = Depends(get_session)):
    try:
        order_repository = OrderRepository(session=session)
        usecase = ListAllOrdersUseCase(order_repository=order_repository)
        output = usecase.execute()
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/{order_id}", status_code=200)
def find_order(order_id: UUID, user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        order_repository = OrderRepository(session=session)
        usecase = FindOrderUseCase(order_repository=order_repository)
        output = usecase.execute(input=FindOrderInputDto(id=order_id, user_id=user_id))
        return output
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.patch("/internal/{order_id}", status_code=200)
def update_order(request: UpdateOrderInputDto, order_id: UUID, user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        request.id = order_id
        request.user_id = user_id
        order_repository = OrderRepository(session=session)
        usecase = UpdateOrderUseCase(order_repository=order_repository)
        output = usecase.execute(input=UpdateOrderInputDto(id=request.id, user_id=request.user_id, total_price=request.total_price, type=request.type, status=request.status, offer_id=request.offer_id))
        return output
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
# @router.delete("/", status_code=200)
# def delete_all_orders(session: Session = Depends(get_session)):
#     try:
#         order_repository = OrderRepository(session=session)
#         usecase = DeleteAllOrdersUseCase(order_repository=order_repository)
#         usecase.execute()
#         return {"message": "All orders deleted"}
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e