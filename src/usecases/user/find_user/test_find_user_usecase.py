from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.user.find_user.find_user_dto import (FindUserInputDto,
                                                   FindUserOutputDto)
from usecases.user.find_user.find_user_usecase import FindUserUseCase


@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def find_user_usecase(user_repository):
    return FindUserUseCase(user_repository)

def test_find_user_success(find_user_usecase, user_repository):
    user_id = uuid4()
    user = User(id=user_id, name="Test User", email="test@example.com", age=30, gender=UserGender.FEMALE, phone_number="1234567890", password="password")
    user_repository.find_user.return_value = user
    
    input_dto = FindUserInputDto(id=user_id)
    
    output_dto = find_user_usecase.execute(input=input_dto)
    
    assert output_dto.id == user_id
    assert output_dto.name == "Test User"
    assert output_dto.email == "test@example.com"
    assert output_dto.age == 30
    assert output_dto.gender == UserGender.FEMALE
    assert output_dto.phone_number == "1234567890"
    assert output_dto.password == "password"
    user_repository.find_user.assert_called_once_with(user_id=user_id)

def test_find_user_not_found(find_user_usecase, user_repository):
    user_id = uuid4()
    user_repository.find_user.return_value = None
    
    input_dto = FindUserInputDto(id=user_id)
    
    with pytest.raises(ValueError) as excinfo:
        find_user_usecase.execute(input=input_dto)
    assert str(excinfo.value) == f"User with id '{user_id}' not found"
    user_repository.find_user.assert_called_once_with(user_id=user_id)