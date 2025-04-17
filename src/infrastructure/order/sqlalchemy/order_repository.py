from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.order.order_entity import Order
from domain.order.order_repository_interface import OrderRepositoryInterface
from domain.order.order_status_enum import OrderStatus
from infrastructure.order.sqlalchemy.order_model import OrderModel


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order: Order):
        order_model = OrderModel(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=order.total_price, status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)
        self.session.add(order_model)
        await self.session.commit()
        await self.session.refresh(order_model)

        return Order(
            id=order.id, 
            user_id=order.user_id, 
            cart_id=order.cart_id, 
            total_price=order.total_price, 
            type=order.type,
            status=order.status, 
            created_at=order.created_at, 
            updated_at=order.updated_at, 
            offer_id=order.offer_id
        )

    async def find_order(self, order_id: UUID, user_id: UUID) -> Order:
        result = await self.session.execute(
            select(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == user_id)
        )
        order = result.scalars().first()

        if not order:
            return None
        
        return Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)

    async def find_order_by_cart_id(self, cart_id: UUID) -> Order:
        result = await self.session.execute(
            select(OrderModel).filter(OrderModel.cart_id == cart_id)
        )
        order = result.scalars().first()

        if not order:
            return None
        
        return Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)

    async def update_order(self, order: Order) -> Order:
        stmt = select(OrderModel).filter(OrderModel.id == order.id)
        result = await self.session.execute(stmt)
        order_model = result.scalars().first()
        
        if order_model:
            order_model.type = order.type
            order_model.total_price = order.total_price
            order_model.status = OrderStatus(order.status)
            order_model.updated_at = datetime.now()
            await self.session.commit()
        
        return order
    
    async def list_orders(self, user_id) -> List[Order]:
        result = await self.session.execute(
            select(OrderModel).filter(OrderModel.user_id == user_id)
        )
        orders = result.scalars().all()

        if orders is None:
            return None
        
        return [Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id) for order in orders]
        
    async def list_all_orders(self) -> List[Order]:
        result = await self.session.execute(select(OrderModel))
        orders = result.scalars().all()

        if orders is None:
            return None
        
        return [Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id) for order in orders]

    async def remove_order(self, order_id: UUID) -> UUID:
        # Need to provide user_id for find_order
        result = await self.session.execute(
            select(OrderModel).filter(OrderModel.id == order_id)
        )
        order = result.scalars().first()

        if not order:
            return None
            
        await self.session.delete(order)
        await self.session.commit()

        return order.id
        
    async def delete_all_orders(self) -> None:
        await self.session.execute("DELETE FROM orders")
        await self.session.commit()
        return None