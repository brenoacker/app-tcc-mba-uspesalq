import asyncio
import pytest
from unittest.mock import AsyncMock

class CartItem:
    def __init__(self, id, cart_id, product_id, quantity):
        self.id = id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

class ListItemsByUserInputDto:
    def __init__(self, user_id):
        self.user_id = user_id

class ListItemsByUserDto:
    def __init__(self, id, cart_id, product_id, quantity):
        self.id = id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

class ListItemsByUserOutputDto:
    def __init__(self, items):
        self.items = items

class ListItemsByUserUseCase:
    def __init__(self, cart_item_repository):
        self.cart_item_repository = cart_item_repository

    async def execute(self, input: ListItemsByUserInputDto) -> ListItemsByUserOutputDto:
        
        items = await self.cart_item_repository.list_items_by_user(user_id=input.user_id)
        
        return ListItemsByUserOutputDto(items=[
            ListItemsByUserDto(
                id=item.id, 
                cart_id=item.cart_id, 
                product_id=item.product_id, 
                quantity=item.quantity
            ) for item in items
        ])

def async_return(value):
    mock = AsyncMock()
    mock.return_value = value
    return mock

@pytest.mark.asyncio
async def test_list_items_by_user_success():
    # Arrange
    cart_item_repository = AsyncMock()
    cart_item_repository.list_items_by_user = async_return([
        CartItem(id=1, cart_id=2, product_id=3, quantity=2),
        CartItem(id=4, cart_id=2, product_id=5, quantity=3)
    ])
    
    use_case = ListItemsByUserUseCase(cart_item_repository)
    input_dto = ListItemsByUserInputDto(user_id=123)
    
    # Act
    output_dto = await use_case.execute(input=input_dto)
    
    # Assert
    assert len(output_dto.items) == 2
    assert output_dto.items[0].quantity == 2
    assert output_dto.items[1].quantity == 3
    cart_item_repository.list_items_by_user.assert_awaited_once_with(user_id=123) 