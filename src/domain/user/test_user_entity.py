from uuid import UUID, uuid4

import pytest

from domain.user.user_entity import User
from domain.user.user_gender_enum import UserGender


def test_user_creation():
    user_id = uuid4()
    name = "Test User"
    email = "test@example.com"
    age = 25
    gender = UserGender.MALE
    phone_number = "1234567890"
    password = "securepassword"

    user = User(id=user_id, name=name, email=email, age=age, gender=gender, phone_number=phone_number, password=password)

    assert user.id == user_id
    assert user.name == name
    assert user.email == email
    assert user.phone_number == phone_number
    assert user.password == password

def test_user_with_invalid_age():
    user_id = uuid4()
    name = "Test User"
    email = "test@example.com"
    age = "1"
    gender = UserGender.MALE
    phone_number = "1234567890"
    password = "securepassword"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email=email, age=age, gender=gender, phone_number=phone_number, password=password)
    assert str(excinfo.value) == "age must be an integer"

def test_user_with_age_under_18():
    user_id = uuid4()
    name = "Test User"
    email = "test@example.com"
    age = 15
    gender = UserGender.MALE
    phone_number = "1234567890"
    password = "securepassword"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email=email, age=age, gender=gender, phone_number=phone_number, password=password)
    assert str(excinfo.value) == "age must be greater than 18"

def test_user_with_invalid_gender():
    user_id = uuid4()
    name = "Test User"
    email = "test@example.com"
    age = 20
    gender = "supermale"
    phone_number = "1234567890"
    password = "securepassword"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email=email, age=age, gender=gender, phone_number=phone_number, password=password)
    assert str(excinfo.value) == "gender must be an instance of UserGender"

def test_user_invalid_id():
    name = "Test User"
    email = "test@example.com"
    age = 25
    gender = UserGender.MALE
    phone_number = "1234567890"
    password = "securepassword"

    with pytest.raises(Exception) as excinfo:
        User(id="invalid_uuid", name=name, email=email, age=age, gender=gender, phone_number=phone_number, password=password)
    assert str(excinfo.value) == "id must be an UUID"

def test_user_invalid_name():
    user_id = uuid4()
    email = "test@example.com"
    age = 25
    gender = UserGender.MALE
    phone_number = "1234567890"
    password = "securepassword"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name="", email=email, age=age, gender=gender, phone_number=phone_number, password=password)
    assert str(excinfo.value) == "name is required"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=None, email=email, age=age, gender=gender, phone_number=phone_number, password=password)
    assert str(excinfo.value) == "name is required"

def test_user_invalid_email():
    user_id = uuid4()
    name = "Test User"
    age = 25
    gender = UserGender.MALE
    phone_number = "1234567890"
    password = "securepassword"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email="", age=age, gender=gender, phone_number=phone_number, password=password)
    assert str(excinfo.value) == "email is required"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email=None, age=age, gender=gender, phone_number=phone_number, password=password)
    assert str(excinfo.value) == "email is required"

def test_user_invalid_phone_number():
    user_id = uuid4()
    name = "Test User"
    email = "test@example.com"
    age = 25
    gender = UserGender.MALE
    password = "securepassword"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email=email, age=age, gender=gender, phone_number="", password=password)
    assert str(excinfo.value) == "phone_number is required"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email=email, age=age, gender=gender, phone_number=None, password=password)
    assert str(excinfo.value) == "phone_number is required"

def test_user_invalid_password():
    user_id = uuid4()
    name = "Test User"
    email = "test@example.com"
    age = 25
    gender = UserGender.MALE
    phone_number = "1234567890"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email=email, age=age, gender=gender, phone_number=phone_number, password="")
    assert str(excinfo.value) == "password is required and length must be greater than 4"

    with pytest.raises(Exception) as excinfo:
        User(id=user_id, name=name, email=email, age=age, gender=gender, phone_number=phone_number, password="1234")
    assert str(excinfo.value) == "password is required and length must be greater than 4"