import uuid
from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from domain.order.order_status_enum import OrderStatus
from domain.order_item.order_item_entity import OrderItem
from domain.product.product_entity import Product


class Order:
    id: UUID
    user_id: UUID
    offer_id: UUID
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: UUID, user_id: UUID, items: List[OrderItem], status: OrderStatus, created_at: datetime, updated_at: datetime, offer_id: UUID = None):
        self.id = id
        self.user_id = user_id
        self.offer_id = offer_id
        self.items = items
        self.total_amount = self.calculate_total_amount()
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.user_id, UUID):
            raise Exception("user_id must be an UUID")
        
        if not isinstance(self.items, list) or not all(isinstance(item, OrderItem) for item in self.items):
            raise Exception("items must be a list of OrderItem objects")
        
        if len(self.items) == 0:
            raise Exception("items cannot be empty")
        
        if not isinstance(self.total_amount, (float, int)):
            raise Exception("total_amount must be float or int")
        
        if self.total_amount < 0:
            raise Exception("total_amount must be a non-negative number")
        
        if not isinstance(self.status, OrderStatus):
            raise Exception("status must be an instance of OrderStatus")
        
        if not isinstance(self.created_at, datetime):
            raise Exception("created_at must be a datetime object")
        
        if not isinstance(self.updated_at, datetime):
            raise Exception("updated_at must be a datetime object")
        
        if self.offer_id is not None and not isinstance(self.offer_id, UUID):
            raise Exception("offer_id must be an UUID or None")

    def calculate_total_amount(self):
        return sum(item.price * item.quantity for item in self.items)