from datetime import datetime
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.order.order_entity import Order
from domain.order.order_repository_interface import OrderRepositoryInterface
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from infrastructure.api.cache import async_cached, invalidate_cache
from infrastructure.order.sqlalchemy.order_model import OrderModel


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    @invalidate_cache(key_prefix='order')
    async def create_order(self, order: Order):
        order_model = OrderModel(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=order.total_price, status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)
        self.session.add(order_model)
        await self.session.commit()
        # Removendo a chamada para refresh que adiciona uma consulta extra
        return order

    @async_cached(ttl=300, prefix='order')
    async def find_order(self, order_id: UUID, user_id: UUID) -> Order:
        result = await self.session.execute(
            select(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == user_id)
        )
        order = result.scalars().first()

        if not order:
            return None
        
        return Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)

    @async_cached(ttl=300, prefix='order')
    async def find_order_by_cart_id(self, cart_id: UUID) -> Order:
        result = await self.session.execute(
            select(OrderModel).filter(OrderModel.cart_id == cart_id)
        )
        order = result.scalars().first()

        if not order:
            return None
        
        return Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)

    @invalidate_cache(key_prefix='order')
    async def update_order(self, order: Order) -> Order:
        try:
            await self.session.execute(
                update(OrderModel)
                .where(OrderModel.id == order.id)
                .values(
                    type=order.type,
                    total_price=order.total_price,
                    status=OrderStatus(order.status),
                    updated_at=datetime.now()
                )
            )
            await self.session.commit()
            
            # Não precisamos fazer uma nova consulta, já temos as informações do order
            return order
        except Exception as e:
            await self.session.rollback()
            raise e
    
    @async_cached(ttl=120, prefix='order')
    async def list_orders(self, user_id, page: int = 1, page_size: int = 20) -> Dict:
        """
        Lista pedidos de um usuário com paginação.
        
        Args:
            user_id: ID do usuário
            page: Página atual (começa em 1)
            page_size: Tamanho da página
            
        Returns:
            Dict contendo os pedidos paginados e metadados da paginação
        """
        # Calcula o offset baseado na página
        offset = (page - 1) * page_size
        
        # Consulta para contar o total de registros
        count_query = select(func.count()).select_from(OrderModel).filter(OrderModel.user_id == user_id)
        count_result = await self.session.execute(count_query)
        total_count = count_result.scalar()
        
        # Consulta para obter os dados paginados
        query = (
            select(OrderModel)
            .filter(OrderModel.user_id == user_id)
            .order_by(OrderModel.created_at.desc())  # Ordena por data de criação (mais recentes primeiro)
            .offset(offset)
            .limit(page_size)
        )
        
        result = await self.session.execute(query)
        orders = result.scalars().all()
        
        if not orders:
            return {
                "items": [],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size
                }
            }
        
        order_list = [
            Order(
                id=order.id, 
                user_id=order.user_id, 
                cart_id=order.cart_id, 
                type=order.type, 
                total_price=float(order.total_price), 
                status=order.status, 
                created_at=order.created_at, 
                updated_at=order.updated_at, 
                offer_id=order.offer_id
            ) 
            for order in orders
        ]
        
        return {
            "items": order_list,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": (total_count + page_size - 1) // page_size
            }
        }
        
    @async_cached(ttl=60, prefix='order')
    async def list_all_orders(self, page: int = 1, page_size: int = 50, status: Optional[OrderStatus] = None) -> Dict:
        """
        Lista todos os pedidos com paginação e filtragem opcional por status.
        
        Args:
            page: Página atual (começa em 1)
            page_size: Tamanho da página
            status: Status para filtrar os pedidos (opcional)
            
        Returns:
            Dict contendo os pedidos paginados e metadados da paginação
        """
        # Calcula o offset baseado na página
        offset = (page - 1) * page_size
        
        # Prepara a consulta base
        base_query = select(OrderModel)
        count_query = select(func.count()).select_from(OrderModel)
        
        # Aplica filtro por status se fornecido
        if status is not None:
            base_query = base_query.filter(OrderModel.status == status)
            count_query = count_query.filter(OrderModel.status == status)
        
        # Consulta para contar o total de registros
        count_result = await self.session.execute(count_query)
        total_count = count_result.scalar()
        
        # Consulta para obter os dados paginados
        query = (
            base_query
            .order_by(OrderModel.created_at.desc())  # Ordena por data de criação (mais recentes primeiro)
            .offset(offset)
            .limit(page_size)
        )
        
        result = await self.session.execute(query)
        orders = result.scalars().all()
        
        if not orders:
            return {
                "items": [],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size,
                    "status_filter": status.value if status else None
                }
            }
        
        order_list = [
            Order(
                id=order.id, 
                user_id=order.user_id, 
                cart_id=order.cart_id, 
                type=order.type, 
                total_price=float(order.total_price), 
                status=order.status, 
                created_at=order.created_at, 
                updated_at=order.updated_at, 
                offer_id=order.offer_id
            ) 
            for order in orders
        ]
        
        return {
            "items": order_list,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": (total_count + page_size - 1) // page_size,
                "status_filter": status.value if status else None
            }
        }

    @invalidate_cache(key_prefix='order')
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
        
    @invalidate_cache(key_prefix='order')
    async def delete_all_orders(self) -> None:
        await self.session.execute(
            OrderModel.__table__.delete()
        )
        await self.session.commit()
        return None