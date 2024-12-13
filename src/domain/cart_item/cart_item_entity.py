from uuid import UUID


class CartItem:

    id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int

    def __init__(self, id: UUID, user_id: UUID, product_id: UUID, quantity: int):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.user_id, UUID):
            raise Exception("user_id must be an UUID")
        
        if not isinstance(self.product_id, UUID):
            raise Exception("product_id must be an UUID")
        
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise Exception("quantity must be a positive integer")


    def item_quantity(self):
        return self.quantity
    