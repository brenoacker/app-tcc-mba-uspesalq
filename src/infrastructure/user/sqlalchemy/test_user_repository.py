from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender
from infrastructure.user.sqlalchemy.user_model import UserModel
from infrastructure.user.sqlalchemy.user_repository import UserRepository


@pytest.fixture
def session():
    return MagicMock()

@pytest.fixture
def user_repository(session):
    return UserRepository(session)

def test_add_user(user_repository, session):
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

    added_user = user_repository.add_user(user)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    assert added_user.id == user.id
    assert added_user.name == user.name
    assert added_user.email == user.email
    assert added_user.age == user.age
    assert added_user.gender == user.gender
    assert added_user.phone_number == user.phone_number
    assert added_user.password == user.password

def test_find_user(user_repository, session):
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
    session.query().filter().first.return_value = user_model

    found_user = user_repository.find_user(user_id)

    assert found_user.id == user_id
    assert found_user.name == user_model.name
    assert found_user.email == user_model.email
    assert found_user.age == user_model.age
    assert found_user.gender == user_model.gender
    assert found_user.phone_number == user_model.phone_number
    assert found_user.password == user_model.password

def test_find_user_not_found(user_repository, session):
    user_id = uuid4()
    session.query().filter().first.return_value = None

    with pytest.raises(ValueError, match=f"User with id '{user_id}' not found"):
        user_repository.find_user(user_id)

def test_find_user_by_email(user_repository, session):
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
    session.query().filter().first.return_value = user_model

    found_user = user_repository.find_user_by_email(email)

    assert found_user.id == user_id
    assert found_user.name == user_model.name
    assert found_user.email == user_model.email
    assert found_user.age == user_model.age
    assert found_user.gender == user_model.gender
    assert found_user.phone_number == user_model.phone_number
    assert found_user.password == user_model.password

def test_find_user_by_email_not_found(user_repository, session):
    email = "john.doe@example.com"
    session.query().filter().first.return_value = None

    found_user = user_repository.find_user_by_email(email)

    assert found_user is None

def test_list_users(user_repository, session):
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
    session.query().all.return_value = [user_model_1, user_model_2]

    users = user_repository.list_users()

    assert len(users) == 2
    assert users[0].id == user_model_1.id
    assert users[1].id == user_model_2.id

def test_list_users_empty(user_repository, session):
    session.query().all.return_value = []

    users = user_repository.list_users()

    assert users is None

def test_update_user(user_repository, session):
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

    user_repository.update_user(user)

    session.query().filter().update.assert_called_once()
    session.commit.assert_called_once()

def test_delete_user(user_repository, session):
    user_id = uuid4()

    user_repository.delete_user(user_id)

    session.query().filter().delete.assert_called_once()
    session.commit.assert_called_once()