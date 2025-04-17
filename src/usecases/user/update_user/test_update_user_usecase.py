from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from usecases.user.update_user.update_user_dto import (UpdateUserInputDto)
from usecases.user.update_user.update_user_usecase import UpdateUserUseCase


@pytest.fixture
def user_repository():
    return Mock()

@pytest.fixture
def update_user_usecase(user_repository):
    return UpdateUserUseCase(user_repository)

def test_update_user_success(update_user_usecase, user_repository):
    user_id = uuid4()
    user_name = "Updated User"
    user_email = "updated@example.com"
    user_age = 35
    user_gender = UserGender.MALE
    user_phone_number = "0987654321"
    user_password = "newpassword"
    user = User(id=user_id, name=user_name, email=user_email, age=user_age, gender=user_gender, phone_number=user_phone_number, password=user_password)
    user_repository.update_user.return_value = user
    
    input_dto = UpdateUserInputDto(name=user_name, email=user_email, age=user_age, gender=user_gender, phone_number=user_phone_number, password=user_password)
    
    output_dto = update_user_usecase.execute(id=user_id, input=input_dto)
    
    assert output_dto.id == user_id
    assert output_dto.name == user_name
    assert output_dto.email == user_email
    assert output_dto.age == user_age
    assert output_dto.gender == user_gender
    assert output_dto.phone_number == user_phone_number
    assert output_dto.password == user_password
    user_repository.update_user.assert_called_once()

def test_update_user_not_found(update_user_usecase, user_repository):
    user_id = uuid4()
    user_repository.find_user.return_value = None
    
    input_dto = UpdateUserInputDto(name="Updated User", email="updated@example.com", age=35, gender=UserGender.MALE, phone_number="0987654321", password="newpassword")
    
    with pytest.raises(ValueError) as excinfo:
        update_user_usecase.execute(id=user_id, input=input_dto)
    assert str(excinfo.value) == f"User with id '{user_id}' not found"