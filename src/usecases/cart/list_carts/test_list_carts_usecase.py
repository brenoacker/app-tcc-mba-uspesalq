from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.cart.cart_entity import Cart
from usecases.cart.list_carts.list_carts_dto import (ListCartsDto,
                                                     ListCartsInputDto,
                                                     ListCartsOutputDto)
from usecases.cart.list_carts.list_carts_usecase import ListCartsUseCase


@pytest.fixture
def cart_repository():
    return Mock()

@pytest.fixture
def list_carts_usecase(cart_repository):
    return ListCartsUseCase(cart_repository)

def test_list_carts_success(list_carts_usecase, cart_repository):
    user_id = uuid4()
    cart_repository.list_carts.return_value = [
        Cart(id=uuid4(), user_id=user_id, total_price=100.0),
        Cart(id=uuid4(), user_id=user_id, total_price=200.0)
    ]
    
    input_dto = ListCartsInputDto(user_id=user_id)
    
    output_dto = list_carts_usecase.execute(input=input_dto)
    
    assert len(output_dto.carts) == 2
    assert output_dto.carts[0].total_price == 100.0
    assert output_dto.carts[1].total_price == 200.0
    cart_repository.list_carts.assert_called_once_with(user_id=user_id)

def test_list_carts_no_carts_found(list_carts_usecase, cart_repository):
    user_id = uuid4()
    cart_repository.list_carts.return_value = []
    
    input_dto = ListCartsInputDto(user_id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        list_carts_usecase.execute(input=input_dto)
    assert str(excinfo.value) == "No carts found"
    cart_repository.list_carts.assert_called_once_with(user_id=user_id)