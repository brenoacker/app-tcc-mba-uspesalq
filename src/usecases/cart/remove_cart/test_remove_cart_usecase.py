from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.cart.cart_entity import Cart
from usecases.cart.remove_cart.remove_cart_dto import (RemoveCartInputDto,
                                                       RemoveCartOutputDto)
from usecases.cart.remove_cart.remove_cart_usecase import RemoveCartUseCase


@pytest.fixture
def cart_repository():
    return Mock()

@pytest.fixture
def remove_cart_usecase(cart_repository):
    return RemoveCartUseCase(cart_repository)

def test_remove_cart_success(remove_cart_usecase, cart_repository):
    cart_id = uuid4()
    user_id = uuid4()
    cart_repository.find_cart.return_value = Cart(id=cart_id, user_id=user_id, total_price=100.0)
    
    input_dto = RemoveCartInputDto(id=cart_id, user_id=user_id)
    
    output_dto = remove_cart_usecase.execute(input=input_dto)
    
    assert output_dto.id == cart_id
    cart_repository.find_cart.assert_called_once_with(cart_id=cart_id, user_id=user_id)
    cart_repository.remove_cart.assert_called_once_with(cart_id=cart_id)

def test_remove_cart_not_found(remove_cart_usecase, cart_repository):
    cart_id = uuid4()
    user_id = uuid4()
    cart_repository.find_cart.return_value = None
    
    input_dto = RemoveCartInputDto(id=cart_id, user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        remove_cart_usecase.execute(input=input_dto)
    assert str(excinfo.value) == "Cart not found"
    cart_repository.find_cart.assert_called_once_with(cart_id=cart_id, user_id=user_id)
    cart_repository.remove_cart.assert_not_called()