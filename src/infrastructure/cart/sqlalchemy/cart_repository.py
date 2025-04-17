from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.cart.cart_entity import Cart
from domain.cart.cart_repository_interface import CartRepositoryInterface
from infrastructure.cart.sqlalchemy.cart_model import CartModel


class CartRepository(CartRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_cart(self, cart_id: UUID, user_id: UUID):
        result = await self.session.execute(
            select(CartModel).filter(CartModel.id == cart_id, CartModel.user_id == user_id)
        )
        cart = result.scalars().first()

        if not cart:
            return None

        return Cart(id=cart.id, user_id=cart.user_id, total_price=cart.total_price)

    async def add_cart(self, cart: Cart):
        cart_model = CartModel(
            id=cart.id,
            user_id=cart.user_id,
            total_price=cart.total_price
        )

        self.session.add(cart_model)
        await self.session.commit()

        return None

    async def update_cart(self, cart: Cart) -> Cart:
        await self.session.execute(
            select(CartModel).filter(CartModel.id == cart.id).update(
                {
                    "total_price": cart.total_price
                }
            )
        )
        await self.session.commit()

        result = await self.session.execute(
            select(CartModel).filter(CartModel.id == cart.id)
        )
        updated_cart_model = result.scalars().first()

        updated_cart = Cart(
            id=updated_cart_model.id,
            user_id=updated_cart_model.user_id,
            total_price=updated_cart_model.total_price
        )

        return updated_cart

    async def remove_cart(self, cart_id: UUID):
        await self.session.execute(
            select(CartModel).filter(CartModel.id == cart_id).delete()
        )
        await self.session.commit()

        return None

    async def list_carts(self, user_id: UUID):
        result = await self.session.execute(
            select(CartModel).filter(CartModel.user_id == user_id)
        )
        carts = result.scalars().all()

        if not carts:
            return None

        return [Cart(id=cart.id, user_id=cart.user_id, total_price=cart.total_price) for cart in carts]

    async def delete_all_carts(self):
        await self.session.execute(select(CartModel).delete())
        await self.session.commit()

        return None