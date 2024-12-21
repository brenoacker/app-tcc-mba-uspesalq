import uuid
from unittest.mock import Mock

import pytest

from usecases.user.delete_user.delete_user_dto import (DeleteUserInputDto,
                                                       DeleteUserOutputDto)
from usecases.user.delete_user.delete_user_usecase import DeleteUserUseCase


@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def delete_user_usecase(user_repository):
    return DeleteUserUseCase(user_repository=user_repository)

def test_delete_user_success(delete_user_usecase, user_repository):
    # Arrange
    input_dto = DeleteUserInputDto(id=uuid.uuid4())
    user_repository.delete_user.return_value = None

    # Act
    output_dto = delete_user_usecase.execute(input=input_dto)

    # Assert
    assert isinstance(output_dto, DeleteUserOutputDto)
    user_repository.delete_user.assert_called_once_with(user_id=input_dto.id)