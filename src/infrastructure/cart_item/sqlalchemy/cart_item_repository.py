from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.cart_item.cart_item_entity import CartItem
from domain.cart_item.cart_item_repository_interface import \
    CartItemRepositoryInterface
from infrastructure.cart.sqlalchemy.cart_model import CartModel
from infrastructure.cart_item.sqlalchemy.cart_item_model import CartItemModel
from infrastructure.logging_config import logger
from usecases.cart_item.list_items.list_items_dto import ListItemsOutputDto


class CartItemRepository(CartItemRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_item(self, cart_item: CartItem) -> None:

        cart_item_model = CartItemModel(
            id=cart_item.id, 
            cart_id=cart_item.cart_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )

        self.session.add(cart_item_model)
        await self.session.commit()

        return None

    async def find_item(self, item_id: UUID) -> Optional[CartItem]:
        result = await self.session.execute(
            select(CartItemModel).filter(CartItemModel.id == item_id)
        )
        cart_item_in_db = result.scalars().first()
        
        if not cart_item_in_db:
            return None
        
        cart_item = CartItem(
            id=cart_item_in_db.id,
            cart_id=cart_item_in_db.cart_id,
            product_id=cart_item_in_db.product_id,
            quantity=cart_item_in_db.quantity
        )

        return cart_item
    
    async def update_item(self, item: CartItem) -> None:
        stmt = select(CartItemModel).filter(CartItemModel.id == item.id)
        result = await self.session.execute(stmt)
        cart_item_model = result.scalars().first()
        
        if cart_item_model:
            cart_item_model.cart_id = item.cart_id
            cart_item_model.product_id = item.product_id
            cart_item_model.quantity = item.quantity
            await self.session.commit()

        return None

    async def remove_item(self, item_id: UUID) -> None:
        stmt = select(CartItemModel).filter(CartItemModel.id == item_id)
        result = await self.session.execute(stmt)
        cart_item = result.scalars().first()
        
        if cart_item:
            await self.session.delete(cart_item)
            await self.session.commit()

        return None

    async def list_items(self) -> Optional[List[CartItem]]:
        result = await self.session.execute(select(CartItemModel))
        cart_items_in_db = result.scalars().all()

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
    
    async def list_items_by_user(self, user_id: UUID) -> List[CartItem]:
        result = await self.session.execute(
            select(CartItemModel)
            .join(CartModel, CartItemModel.cart_id == CartModel.id)
            .filter(CartModel.user_id == user_id)
        )
        cart_items_in_db = result.scalars().all()

        cart_items = []

        for cart_item_in_db in cart_items_in_db:
            cart_items.append(CartItem(
                id=cart_item_in_db.id,
                cart_id=cart_item_in_db.cart_id,
                product_id=cart_item_in_db.product_id,
                quantity=cart_item_in_db.quantity
            ))

        return cart_items
    
    async def find_items_by_cart_id(self, cart_id: UUID) -> Optional[List[CartItem]]:
        result = await self.session.execute(
            select(CartItemModel).filter(CartItemModel.cart_id == cart_id)
        )
        cart_items_in_db = result.scalars().all()

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