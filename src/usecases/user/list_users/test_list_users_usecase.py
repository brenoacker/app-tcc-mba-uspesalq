from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.user.list_users.list_users_usecase import ListUsersUseCase


@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def list_users_usecase(user_repository):
    return ListUsersUseCase(user_repository)

@pytest.mark.asyncio
async def test_list_users_success(list_users_usecase, user_repository):
    user_id = uuid4()
    user = User(id=user_id, name="Test User", email="test@example.com", age=30, gender=UserGender.MALE, phone_number="1234567890", password="password")
    user_repository.list_users = async_return([user])
    
    # Substituindo run_async por await
    output_dto = await list_users_usecase.execute()
    
    assert len(output_dto.users) == 1
    assert output_dto.users[0].id == user_id
    assert output_dto.users[0].name == "Test User"
    assert output_dto.users[0].email == "test@example.com"
    assert output_dto.users[0].age == 30
    assert output_dto.users[0].gender == UserGender.MALE
    assert output_dto.users[0].phone_number == "1234567890"
    assert output_dto.users[0].password == "password"
    user_repository.list_users.await_count == 1

@pytest.mark.asyncio
async def test_list_users_empty(list_users_usecase, user_repository):
    user_repository.list_users = async_return([])
    
    # Substituindo run_async por await
    output_dto = await list_users_usecase.execute()
    
    assert len(output_dto.users) == 0
    assert user_repository.list_users.await_count == 1