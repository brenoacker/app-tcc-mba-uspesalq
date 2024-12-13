from uuid import UUID


class OrderItem:

    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    price: float

    def __init__(self, id: UUID, order_id: UUID, product_id: UUID, quantity: int, price: float):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.order_id, UUID):
            raise Exception("order_id must be an UUID")
        
        if not isinstance(self.product_id, UUID):
            raise Exception("product_id must be an UUID")
        
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise Exception("quantity must be a positive integer")
        
        if not isinstance(self.price, (float, int)) or self.price < 0:
            raise Exception("price must be a non-negative number")