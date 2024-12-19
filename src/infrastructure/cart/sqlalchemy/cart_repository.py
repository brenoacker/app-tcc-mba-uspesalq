from uuid import UUID

from sqlalchemy import and_

from domain.cart.cart_entity import Cart
from domain.cart.cart_repository_interface import CartRepositoryInterface
from infrastructure.cart.sqlalchemy.cart_model import CartModel


class CartRepository(CartRepositoryInterface):

    def __init__(self, session):
        self.session = session

    def find_cart(self, cart_id: UUID, user_id: UUID):
        cart = self.session.query(CartModel).filter(
            and_(
                CartModel.id == cart_id,
                CartModel.user_id == user_id
            )
        ).first()
        
        if not cart:
            return None
        
        return Cart(id=cart.id, user_id=cart.user_id, total_price=cart.total_price)

    def add_cart(self, cart: Cart):
        cart_model = CartModel(
            id=cart.id,
            user_id=cart.user_id,
            total_price=cart.total_price
        )

        self.session.add(cart_model)
        self.session.commit()

        return None

    def update_cart(self, cart: Cart) -> Cart:
        self.session.query(CartModel).filter(CartModel.id == cart.id).update(
            {
                "total_price": cart.total_price
            }
        )
        self.session.commit()

        updated_cart_model = self.session.query(CartModel).filter(CartModel.id == cart.id).first()

        updated_cart = Cart(id=updated_cart_model.id, user_id=updated_cart_model.user_id, total_price=updated_cart_model.total_price)
        
        return updated_cart

    def remove_cart(self, cart_id: UUID):
        self.session.query(CartModel).filter(CartModel.id == cart_id).delete()
        self.session.commit()

        return None
    
    def list_carts(self, user_id: UUID):
        carts = self.session.query(CartModel).filter(CartModel.user_id == user_id).all()
        
        if not carts:
            return None
        
        return [Cart(id=cart.id, user_id=cart.user_id, total_price=cart.total_price) for cart in carts]
    