import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.user.add_user.add_user_dto import (AddUserInputDto,
                                                 AddUserOutputDto)
from usecases.user.add_user.add_user_usecase import AddUserUseCase


@pytest.fixture
def user_repository():
    repo = Mock()
    repo.add_user = AsyncMock()
    return repo

@pytest.fixture
def add_user_usecase(user_repository):
    return AddUserUseCase(user_repository)

@pytest.mark.asyncio
async def test_add_user_success(add_user_usecase, user_repository):
    input_dto = AddUserInputDto(
        name="John Doe",
        email="john.doe@example.com",
        age=25,
        gender="male",
        phone_number="1234567890",
        password="securepassword"
    )
    
    user_id = uuid.uuid4()
    user_repository.add_user = async_return(User(id=user_id, name=input_dto.name, email=input_dto.email, age=input_dto.age, gender=UserGender.MALE, phone_number=input_dto.phone_number, password=input_dto.password))
    
    # Substituindo run_async por await
    output_dto = await add_user_usecase.execute(input=input_dto)
    
    assert output_dto.id is not None
    assert output_dto.name == "John Doe"
    assert output_dto.email == "john.doe@example.com"
    assert output_dto.age == 25
    assert output_dto.gender == UserGender.MALE  # Corrigido para comparar com o enum em vez da string
    assert output_dto.phone_number == "1234567890"
    assert output_dto.password == "securepassword"
    assert user_repository.add_user.await_count == 1