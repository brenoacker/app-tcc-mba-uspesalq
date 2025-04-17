import logging
import traceback
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.api.database import get_session
from infrastructure.cart.sqlalchemy.cart_repository import CartRepository
from infrastructure.offer.sqlalchemy.offer_repository import OfferRepository
from infrastructure.order.sqlalchemy.order_repository import OrderRepository
from infrastructure.user.sqlalchemy.user_repository import UserRepository
from usecases.order.create_order.create_order_dto import CreateOrderInputDto
from usecases.order.create_order.create_order_usecase import CreateOrderUseCase
from usecases.order.find_order.find_order_dto import FindOrderInputDto
from usecases.order.find_order.find_order_usecase import FindOrderUseCase
from usecases.order.list_all_orders.list_all_orders_usecase import \
    ListAllOrdersUseCase
from usecases.order.list_orders.list_orders_dto import ListOrdersInputDto
from usecases.order.list_orders.list_orders_usecase import ListOrdersUseCase

router = APIRouter(prefix="/order", tags=["Order"])

@router.post("/", status_code=201)
async def create_order(request: CreateOrderInputDto, user_id: UUID = Header(...), session: AsyncSession = Depends(get_session)):
    try:
        order_repository = OrderRepository(session=session)
        user_repository = UserRepository(session=session)
        cart_repository = CartRepository(session=session)
        offer_repository = OfferRepository(session=session)
        usecase = CreateOrderUseCase(order_repository=order_repository, user_repository=user_repository, cart_repository=cart_repository, offer_repository=offer_repository)
        if not request.offer_id:
            request.offer_id = None
        output = await usecase.execute(user_id = user_id, input=CreateOrderInputDto(type=request.type,cart_id=request.cart_id, offer_id=request.offer_id))
        return output
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/", status_code=200)
async def list_orders(user_id: UUID = Header(...), session: AsyncSession = Depends(get_session)):
    try:
        order_repository = OrderRepository(session=session)
        usecase = ListOrdersUseCase(order_repository=order_repository)
        output = await usecase.execute(input=ListOrdersInputDto(user_id=user_id))
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/all_orders", status_code=200)
async def list_all_orders(session: AsyncSession = Depends(get_session)):
    try:
        order_repository = OrderRepository(session=session)
        usecase = ListAllOrdersUseCase(order_repository=order_repository)
        output = await usecase.execute()
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/{order_id}", status_code=200)
async def find_order(order_id: UUID, user_id: UUID = Header(...), session: AsyncSession = Depends(get_session)):
    try:
        order_repository = OrderRepository(session=session)
        usecase = FindOrderUseCase(order_repository=order_repository)
        output = await usecase.execute(input=FindOrderInputDto(id=order_id, user_id=user_id))
        return output
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e