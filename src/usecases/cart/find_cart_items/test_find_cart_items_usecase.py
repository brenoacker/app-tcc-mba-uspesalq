# import uuid
# from unittest.mock import Mock, patch

# import pytest

# from domain.cart.cart_entity import Cart
# from domain.cart_item.cart_item_entity import CartItem
# from usecases.cart.find_cart_items.find_cart_items_dto import (
#     FindCartItemDto, FindCartItemsInputDto, FindCartItemsOutputDto)
# from usecases.cart.find_cart_items.find_cart_items_usecase import \
#     FindCartItemsUseCase


# @pytest.fixture
# def cart_repository():
#     return Mock()

# @pytest.fixture
# def cart_item_repository():
#     return Mock()

# @pytest.fixture
# def find_cart_items_usecase(cart_repository, cart_item_repository):
#     return FindCartItemsUseCase(cart_repository, cart_item_repository)

# def test_find_cart_items_success(find_cart_items_usecase, cart_repository, cart_item_repository):
#     cart_id = uuid.uuid4()
#     user_id = uuid.uuid4()
#     cart_repository.find_cart.return_value = Cart(id=cart_id, user_id=user_id, total_price=100.0)
#     cart_item_repository.find_items_by_cart_id.return_value = [
#         CartItem(id=uuid.uuid4(), cart_id=cart_id, product_id=uuid.uuid4(), quantity=2),
#         CartItem(id=uuid.uuid4(), cart_id=cart_id, product_id=uuid.uuid4(), quantity=3)
#     ]
    
#     input_dto = FindCartItemsInputDto(cart_id=cart_id, user_id=user_id)
    
#     output_dto = find_cart_items_usecase.execute(input=input_dto)
    
#     assert output_dto.id == cart_id
#     assert output_dto.user_id == user_id
#     assert output_dto.total_price == 100.0
#     cart_repository.find_cart.assert_called_once_with(cart_id=cart_id, user_id=user_id)
#     cart_item_repository.find_items_by_cart_id.assert_called_once_with(cart_id=cart_id)

# def test_find_cart_items_cart_not_found(find_cart_items_usecase, cart_repository):
#     cart_id = uuid.uuid4()
#     user_id = uuid.uuid4()
#     cart_repository.find_cart.return_value = None
    
#     input_dto = FindCartItemsInputDto(cart_id=cart_id, user_id=user_id)
    
#     with patch('infrastructure.api.config.settings', new=Mock(CONNECTION="mock_connection_string")):
#         with pytest.raises(ValueError) as excinfo:
#             find_cart_items_usecase.execute(input=input_dto)
#     assert str(excinfo.value) == f"Cart not found: {input_dto.cart_id}"
#     cart_repository.find_cart.assert_called_once_with(cart_id=cart_id, user_id=user_id)