# from unittest.mock import Mock, patch
# from uuid import uuid4

# import pytest

# from domain.cart.cart_entity import Cart
# from domain.cart_item.cart_item_entity import CartItem
# from domain.product.product_entity import Product
# from usecases.cart.update_cart.update_cart_dto import (UpdateCartInputDto,
#                                                        UpdateCartItemDto)
# from usecases.cart.update_cart.update_cart_usecase import UpdateCartUseCase


# @pytest.fixture
# def cart_repository():
#     return Mock()

# @pytest.fixture
# def cart_item_repository():
#     return Mock()

# @pytest.fixture
# def product_repository():
#     return Mock()

# @pytest.fixture
# def update_cart_usecase(cart_repository, cart_item_repository, product_repository):
#     return UpdateCartUseCase(cart_repository, cart_item_repository, product_repository)

# def test_update_cart_success(update_cart_usecase, cart_repository, cart_item_repository, product_repository):
#     user_id = uuid4()
#     cart_id = uuid4()
#     product_id = uuid4()
#     cart_repository.find_cart.return_value = Cart(id=cart_id, user_id=user_id, total_price=100.0)
#     cart_item_repository.find_items_by_cart_id.return_value = [
#         CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=1)
#     ]
#     product_repository.find_product.return_value = Product(id=product_id, name="Test Product", price=50.0, category="Test Category")
    
#     input_dto = UpdateCartInputDto(items=[UpdateCartItemDto(product_id=product_id, quantity=2)])
    
#     output_dto = update_cart_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
    
#     assert output_dto.id == cart_id
#     assert output_dto.total_price == 100.0
#     cart_repository.find_cart.assert_called_once_with(cart_id=cart_id, user_id=user_id)
#     cart_item_repository.find_items_by_cart_id.assert_called_once_with(cart_id=cart_id)
#     product_repository.find_product.assert_called_once_with(product_id=product_id)
#     cart_repository.update_cart.assert_called_once()

# def test_update_cart_not_found(update_cart_usecase, cart_repository):
#     user_id = uuid4()
#     cart_id = uuid4()
#     cart_repository.find_cart.return_value = None
    
#     input_dto = UpdateCartInputDto(items=[])
    
#     with pytest.raises(ValueError) as excinfo:
#         update_cart_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
#     assert str(excinfo.value) == "Cart not found"
#     cart_repository.find_cart.assert_called_once_with(cart_id=cart_id, user_id=user_id)

# def test_update_cart_items_not_found(update_cart_usecase, cart_repository, cart_item_repository):
#     user_id = uuid4()
#     cart_id = uuid4()
#     cart_repository.find_cart.return_value = Cart(id=cart_id, user_id=user_id, total_price=100.0)
#     cart_item_repository.find_items_by_cart_id.return_value = []
    
#     input_dto = UpdateCartInputDto(items=[])
    
#     with pytest.raises(ValueError) as excinfo:
#         update_cart_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
#     assert str(excinfo.value) == "Cart items not found for this cart"
#     cart_repository.find_cart.assert_called_once_with(cart_id=cart_id, user_id=user_id)
#     cart_item_repository.find_items_by_cart_id.assert_called_once_with(cart_id=cart_id)

# def test_update_cart_product_not_found(update_cart_usecase, cart_repository, cart_item_repository, product_repository):
#     user_id = uuid4()
#     cart_id = uuid4()
#     product_id = uuid4()
#     cart_repository.find_cart.return_value = Cart(id=cart_id, user_id=user_id, total_price=100.0)
#     cart_item_repository.find_items_by_cart_id.return_value = [
#         CartItem(id=uuid4(), cart_id=cart_id, product_id=product_id, quantity=1)
#     ]
#     product_repository.find_product.return_value = None
    
#     input_dto = UpdateCartInputDto(items=[UpdateCartItemDto(product_id=product_id, quantity=2)])
    
#     with pytest.raises(ValueError) as excinfo:
#         update_cart_usecase.execute(user_id=user_id, cart_id=cart_id, input=input_dto)
#     assert str(excinfo.value) == f"Product with code '{product_id}' not found"
#     cart_repository.find_cart.assert_called_once_with(cart_id=cart_id, user_id=user_id)
#     cart_item_repository.find_items_by_cart_id.assert_called_once_with(cart_id=cart_id)
#     product_repository.find_product.assert_called_once_with(product_id=product_id)