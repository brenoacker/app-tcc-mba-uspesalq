from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy import select

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from infrastructure.user.sqlalchemy.user_model import UserModel
from infrastructure.user.sqlalchemy.user_repository import UserRepository


@pytest.fixture
def session():
    # Create a MagicMock that properly handles async methods
    mock = MagicMock()
    
    # Configure execute to return a proper async result
    async def mock_execute(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.first.return_value = None
        scalar_result.all.return_value = []
        result.scalars.return_value = scalar_result
        return result
    
    mock.execute = mock_execute
    mock.commit = AsyncMock()
    mock.refresh = AsyncMock()
    return mock

@pytest.fixture
def user_repository(session):
    return UserRepository(session)

@pytest.mark.asyncio
async def test_find_user(user_repository, session):
    user_id = uuid4()
    user_model = UserModel(
        id=user_id,
        name="John Doe",
        email="john.doe@example.com",
        age=30,
        gender=UserGender.MALE,
        phone_number="1234567890",
        password="password"
    )
    
    # Configure a proper async function for this test
    async def mock_execute_with_user(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.first.return_value = user_model
        result.scalars.return_value = scalar_result
        return result
    
    # Replace the session execute method
    session.execute = mock_execute_with_user

    found_user = await user_repository.find_user(user_id)

    assert found_user.id == user_id
    assert found_user.name == user_model.name
    assert found_user.email == user_model.email
    assert found_user.age == user_model.age
    assert found_user.gender == user_model.gender
    assert found_user.phone_number == user_model.phone_number
    assert found_user.password == user_model.password

@pytest.mark.asyncio
async def test_find_user_not_found(user_repository, session):
    user_id = uuid4()
    
    # Set up the execute mock result
    execute_result = MagicMock()
    scalars_result = MagicMock()
    scalars_result.first.return_value = None
    execute_result.scalars.return_value = scalars_result
    session.execute.return_value = async_return(execute_result)

    with pytest.raises(ValueError, match=f"User with id '{user_id}' not found"):
        await user_repository.find_user(user_id)

@pytest.mark.asyncio
async def test_find_user_by_email(user_repository, session):
    user_id = uuid4()
    email = "john.doe@example.com"
    user_model = UserModel(
        id=user_id,
        name="John Doe",
        email=email,
        age=30,
        gender=UserGender.MALE,
        phone_number="1234567890",
        password="password"
    )
    
    # Configure a proper async function for this test
    async def mock_execute_with_user(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.first.return_value = user_model
        result.scalars.return_value = scalar_result
        return result
    
    # Replace the session execute method
    session.execute = mock_execute_with_user

    found_user = await user_repository.find_user_by_email(email)

    assert found_user.id == user_id
    assert found_user.name == user_model.name
    assert found_user.email == user_model.email
    assert found_user.age == user_model.age
    assert found_user.gender == user_model.gender
    assert found_user.phone_number == user_model.phone_number
    assert found_user.password == user_model.password

@pytest.mark.asyncio
async def test_find_user_by_email_not_found(user_repository, session):
    email = "john.doe@example.com"
    
    # Set up the execute mock result
    execute_result = MagicMock()
    scalars_result = MagicMock()
    scalars_result.first.return_value = None
    execute_result.scalars.return_value = scalars_result
    session.execute.return_value = async_return(execute_result)

    found_user = await user_repository.find_user_by_email(email)

    assert found_user is None

@pytest.mark.asyncio
async def test_list_users(user_repository, session):
    user_model_1 = UserModel(
        id=uuid4(),
        name="John Doe",
        email="john.doe@example.com",
        age=30,
        gender=UserGender.MALE,
        phone_number="1234567890",
        password="password"
    )
    user_model_2 = UserModel(
        id=uuid4(),
        name="Jane Doe",
        email="jane.doe@example.com",
        age=25,
        gender=UserGender.FEMALE,
        phone_number="0987654321",
        password="password"
    )
    
    # Configurar mock assíncrono correto para este teste
    async def mock_execute_with_users(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.all.return_value = [user_model_1, user_model_2]
        result.scalars.return_value = scalar_result
        return result
    
    # Substituir session.execute pelo nosso mock personalizado
    session.execute = mock_execute_with_users

    users = await user_repository.list_users()

    assert len(users) == 2
    assert users[0].id == user_model_1.id
    assert users[1].id == user_model_2.id

@pytest.mark.asyncio
async def test_list_users_empty(user_repository, session):
    # Set up the execute mock result
    execute_result = MagicMock()
    scalars_result = MagicMock()
    scalars_result.all.return_value = []
    execute_result.scalars.return_value = scalars_result
    session.execute.return_value = async_return(execute_result)

    users = await user_repository.list_users()

    assert users is None

@pytest.mark.asyncio
async def test_update_user(user_repository, session):
    user_id = uuid4()
    user = User(
        id=user_id,
        name="John Doe",
        email="john.doe@example.com",
        age=30,
        gender=UserGender.MALE,
        phone_number="1234567890",
        password="password"
    )
    
    # Criar um resultado para o execute
    execute_result = MagicMock()
    execute_result.rowcount = 1
    
    # Usar AsyncMock para session.execute e session.commit
    session.execute = AsyncMock(return_value=execute_result)
    session.commit = AsyncMock()

    await user_repository.update_user(user)

    # Verificar se os métodos AsyncMock foram chamados
    assert session.execute.called
    assert session.commit.called

@pytest.mark.asyncio
async def test_delete_user(user_repository, session):
    user_id = uuid4()

    # Criar um model para o usuário
    user_model = UserModel(
        id=user_id,
        name="Test User",
        email="test@example.com",
        age=30,
        gender=UserGender.MALE,
        phone_number="1234567890",
        password="password"
    )

    # Configurar o mock de execute para retornar o user_model
    async def mock_execute(*args, **kwargs):
        result = MagicMock()
        scalar_result = MagicMock()
        scalar_result.first.return_value = user_model
        result.scalars.return_value = scalar_result
        return result
    
    # Substituir o mock padrão pelo específico para este teste
    session.execute = mock_execute
    
    # Configurar session.delete e session.commit como AsyncMock
    session.delete = AsyncMock()
    session.commit = AsyncMock()

    # Executar o método que está sendo testado
    await user_repository.delete_user(user_id)

    # Verificar que os métodos foram chamados corretamente
    session.delete.assert_awaited_once_with(user_model)
    session.commit.assert_awaited_once()