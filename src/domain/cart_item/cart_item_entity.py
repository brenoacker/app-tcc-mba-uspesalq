from uuid import UUID


class CartItem:

    id: UUID
    cart_id: UUID
    product_id: int
    quantity: int

    def __init__(self, id: UUID, cart_id: UUID, product_id: int, quantity: int):
        self.id = id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.cart_id, UUID):
            raise Exception("cart_id must be an UUID")
        
        if not isinstance(self.product_id, int):
            raise Exception("product_id must be an integer")
        
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise Exception("quantity must be a positive integer")


    def item_quantity(self):
        return self.quantity
    