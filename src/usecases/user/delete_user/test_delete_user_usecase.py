import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest

from domain.__seedwork.test_utils import async_return, async_side_effect
from usecases.user.delete_user.delete_user_dto import (DeleteUserInputDto,
                                                       DeleteUserOutputDto)
from usecases.user.delete_user.delete_user_usecase import DeleteUserUseCase


@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def delete_user_usecase(user_repository):
    return DeleteUserUseCase(user_repository=user_repository)

@pytest.mark.asyncio
async def test_delete_user_success(delete_user_usecase, user_repository):
    # Arrange
    input_dto = DeleteUserInputDto(id=uuid.uuid4())
    user_repository.delete_user = async_return(None)

    # Act
    output_dto = await delete_user_usecase.execute(input=input_dto)

    # Assert
    assert isinstance(output_dto, DeleteUserOutputDto)
    user_repository.delete_user.assert_awaited_once_with()