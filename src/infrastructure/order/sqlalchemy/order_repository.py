from datetime import datetime
from typing import List
from uuid import UUID

from domain.order.order_entity import Order
from domain.order.order_repository_interface import OrderRepositoryInterface
from domain.order.order_status_enum import OrderStatus
from domain.order.order_type_enum import OrderType
from infrastructure.order.sqlalchemy.order_model import OrderModel


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, session):
        self.session = session

    def create_order(self, order: Order):
        self.session.add(OrderModel(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=order.total_price, status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id))
        self.session.commit()

        return Order(
            id=order.id, 
            user_id=order.user_id, 
            cart_id=order.cart_id, 
            total_price=order.total_price, 
            type=order.type,
            status=OrderStatus(order.status), 
            created_at=order.created_at, 
            updated_at=order.updated_at, 
            offer_id=order.offer_id
        )

    def find_order(self, order_id: UUID, user_id: UUID) -> Order:

        order =  self.session.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == user_id).first()

        if not order:
            return None
        
        return Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)

    def find_order_by_cart_id(self, cart_id: UUID) -> Order:
        
        order = self.session.query(OrderModel).filter(OrderModel.cart_id == cart_id).first()

        if not order:
            return None
        
        return Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)

    def update_order(self, order: Order) -> Order:

        self.session.query(OrderModel).filter(OrderModel.id == OrderModel.id).update(
            {
                "type": order.type,
                "total_price": float(order.total_price),
                "status": order.status,
                "updated_at": order.updated_at,
            }
        )
        self.session.commit()
        
        return Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id)
    
    def list_orders(self, user_id) -> List[Order]:
        orders: OrderModel = self.session.query(OrderModel).filter(OrderModel.user_id == user_id).all()

        if orders is None:
            return None
        
        return [Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id) for order in orders]
        
    def list_all_orders(self) -> List[Order]:
        orders: OrderModel = self.session.query(OrderModel).all()

        if orders is None:
            return None
        
        return [Order(id=order.id, user_id=order.user_id, cart_id=order.cart_id, type=order.type, total_price=float(order.total_price), status=order.status, created_at=order.created_at, updated_at=order.updated_at, offer_id=order.offer_id) for order in orders]

    def remove_order(self, order_id, user_id) -> UUID:
        order = self.find_order(order_id=order_id, user_id=user_id)

        if not order:
            return None
            
        self.session.delete(order)
        self.session.commit()

        return order.id
    
    def delete_all_orders(self) -> None:
        self.session.query(OrderModel).delete()
        self.session.commit()

        return None