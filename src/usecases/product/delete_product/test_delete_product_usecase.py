import random
from unittest.mock import Mock
from uuid import uuid4

import pytest

from usecases.product.delete_product.delete_product_dto import (
    DeleteProductInputDto, DeleteProductOutputDto)
from usecases.product.delete_product.delete_product_usecase import \
    DeleteProductUseCase


@pytest.fixture
def product_repository():
    return Mock()

@pytest.fixture
def delete_product_usecase(product_repository):
    return DeleteProductUseCase(product_repository)

def test_delete_product_success(delete_product_usecase, product_repository):
    product_id = random.randint(1,10)
    product_repository.delete_product.return_value = None
    
    input_dto = DeleteProductInputDto(id=product_id)
    
    output_dto = delete_product_usecase.execute(input=input_dto)
    
    assert output_dto.id == product_id
    product_repository.delete_product.assert_called_once_with(product_id=product_id)

def test_delete_product_not_found(delete_product_usecase, product_repository):
    product_id = random.randint(1,10)
    product_repository.delete_product.side_effect = ValueError(f"Product with id '{product_id}' not found")
    
    input_dto = DeleteProductInputDto(id=product_id)
    
    with pytest.raises(ValueError) as excinfo:
        delete_product_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"Product with id '{product_id}' not found"
    product_repository.delete_product.assert_called_once_with(product_id=product_id)