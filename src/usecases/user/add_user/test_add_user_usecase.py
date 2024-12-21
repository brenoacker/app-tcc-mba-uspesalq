import uuid
from unittest.mock import Mock

import pytest

from domain.user.user_entity import User
from usecases.user.add_user.add_user_dto import (AddUserInputDto,
                                                 AddUserOutputDto)
from usecases.user.add_user.add_user_usecase import AddUserUseCase


@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def add_user_usecase(user_repository):
    return AddUserUseCase(user_repository=user_repository)

def test_add_user_success(add_user_usecase, user_repository):

    input_dto = AddUserInputDto(
        name="John Doe",
        email="john.doe@example.com",
        age=25,
        gender="male",
        phone_number="1234567890",
        password="securepassword"
    )
    user_repository.add_user.return_value = User(id=uuid.uuid4(), name=input_dto.name, email=input_dto.email, age=input_dto.age, gender=input_dto.gender, phone_number=input_dto.phone_number, password=input_dto.password)

    output_dto = add_user_usecase.execute(input=input_dto)

    assert output_dto.name == input_dto.name
    assert output_dto.email == input_dto.email
    assert output_dto.phone_number == input_dto.phone_number
    assert output_dto.password == input_dto.password
    assert isinstance(output_dto.id, uuid.UUID)
    user_repository.add_user.assert_called_once()