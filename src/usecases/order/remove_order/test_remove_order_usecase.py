from unittest.mock import Mock
from uuid import uuid4

import pytest

from usecases.order.remove_order.remove_order_dto import RemoveOrderInputDto
from usecases.order.remove_order.remove_order_usecase import RemoveOrderUseCase


@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def remove_order_usecase(order_repository):
    return RemoveOrderUseCase(order_repository)

def test_remove_order_success(remove_order_usecase, order_repository):
    order_id = uuid4()
    order_repository.remove_order.return_value = order_id
    
    input_dto = RemoveOrderInputDto(id=order_id)
    
    output_dto = remove_order_usecase.execute(input=input_dto)
    
    assert output_dto.id == order_id
    order_repository.remove_order.assert_called_once_with(order_id=order_id)

def test_remove_order_not_found(remove_order_usecase, order_repository):
    order_id = uuid4()
    order_repository.remove_order.return_value = None
    
    input_dto = RemoveOrderInputDto(id=order_id)
    
    with pytest.raises(ValueError) as excinfo:
        remove_order_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Order with id '{order_id}' not found"
    order_repository.remove_order.assert_called_once_with(order_id=order_id)