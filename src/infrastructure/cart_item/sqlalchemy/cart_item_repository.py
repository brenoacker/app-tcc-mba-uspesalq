from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.orm.session import Session

from domain.cart_item.cart_item_entity import CartItem
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from infrastructure.cart_item.sqlalchemy.cart_item_model import CartItemModel
from infrastructure.logging_config import logger
from usecases.cart_item.list_items.list_items_dto import ListItemsOutputDto


class CartItemRepository(CartItemRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def add_item(self, cart_item: CartItem) -> None:

        cart_item_model = CartItemModel(
            id=cart_item.id, 
            cart_id=cart_item.cart_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )

        self.session.add(cart_item_model)
        self.session.commit()

        return None

    def find_item(self, item_id: UUID) -> Optional[CartItem]:
        cart_item_in_db =  self.session.query(CartItemModel).filter(CartItemModel.id == item_id).first()
        if not cart_item_in_db:
            return None
        
        cart_item = CartItem(
            id=cart_item_in_db.id,
            cart_id=cart_item_in_db.cart_id,
            product_id=cart_item_in_db.product_id,
            quantity=cart_item_in_db.quantity
        )

        return cart_item
    
    def update_item(self, item: CartItem) -> None:

        self.session.query(CartItemModel).filter(CartItemModel.id == item.id).update(
            {
                "cart_id": item.cart_id,
                "product_id": item.product_id,
                "quantity": item.quantity
            }
        )
        self.session.commit()

        return None

    def remove_item(self, item_id: UUID) -> None:

        self.session.query(CartItemModel).filter(CartItemModel.id == item_id).delete()
        self.session.commit()

        return None

    def list_items(self) -> Optional[List[CartItem]]:
        cart_items_in_db = self.session.query(CartItemModel).all()

        logger.info(f"cart_items_in_db: {cart_items_in_db}")

        cart_items = []

        for cart_item_in_db in cart_items_in_db:
            cart_items.append(CartItem(
                id=cart_item_in_db.id,
                cart_id=cart_item_in_db.cart_id,
                product_id=cart_item_in_db.product_id,
                quantity=cart_item_in_db.quantity
            ))
        logger.info(f"cart_items: {cart_items}")

        return cart_items
    
    def list_items_by_user(self, user_id: UUID) -> List[CartItem]:
        cart_items_in_db = self.session.query(CartItemModel).filter(CartItemModel.user_id == user_id).all()

        cart_items = []

        for cart_item_in_db in cart_items_in_db:
            cart_items.append(CartItem(
                id=cart_item_in_db.id,
                cart_id=cart_item_in_db.cart_id,
                product_id=cart_item_in_db.product_id,
                quantity=cart_item_in_db.quantity
            ))

        return cart_items
    
    def find_items_by_cart_id(self, cart_id: UUID) -> Optional[List[CartItem]]:
        cart_items_in_db = self.session.query(CartItemModel).filter(CartItemModel.cart_id == cart_id).all()

        if not cart_items_in_db:
            return None

        cart_items = []

        for cart_item_in_db in cart_items_in_db:
            cart_items.append(CartItem(
                id=cart_item_in_db.id,
                cart_id=cart_item_in_db.cart_id,
                product_id=cart_item_in_db.product_id,
                quantity=cart_item_in_db.quantity
            ))

        return cart_items