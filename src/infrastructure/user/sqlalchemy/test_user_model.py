from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.user.user_gender_enum import UserGender
from infrastructure.api.database import Base
from infrastructure.user.sqlalchemy.user_model import UserGenderType, UserModel

from domain.__seedwork.test_utils import run_async, async_return, async_side_effect


@pytest.fixture
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture
def session(engine):
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.mark.asyncio
async def test_user_model_mapping(session):
    user_id = uuid4()
    user = UserModel(
        id=user_id,
        name="John Doe",
        email="john.doe@example.com",
        age=30,
        gender=UserGender.MALE,
        phone_number="1234567890",
        password="password"
    )
    session.add(user)
    session.commit()

    retrieved_user = session.query(UserModel).filter_by(id=user_id).first()
    assert retrieved_user is not None
    assert retrieved_user.id == user_id
    assert retrieved_user.name == "John Doe"
    assert retrieved_user.email == "john.doe@example.com"
    assert retrieved_user.age == 30
    assert retrieved_user.gender == UserGender.MALE
    assert retrieved_user.phone_number == "1234567890"
    assert retrieved_user.password == "password"

@pytest.mark.asyncio
async def test_user_gender_type():
    user_gender_type = UserGenderType()
    assert user_gender_type.process_bind_param(UserGender.MALE, None) == 'male'
    assert user_gender_type.process_result_value('male', None) == UserGender.MALE

@pytest.mark.asyncio
async def test_process_bind_param():
    user_gender_type = UserGenderType()
    # Teste com valor do tipo UserGender
    assert user_gender_type.process_bind_param(UserGender.MALE, None) == 'male'
    # Teste com valor do tipo string
    assert user_gender_type.process_bind_param('male', None) == 'male'
    # Teste com valor None
    assert user_gender_type.process_bind_param(None, None) is None

@pytest.mark.asyncio
async def test_process_result_value():
    user_gender_type = UserGenderType()
    # Teste com valor do tipo string
    assert user_gender_type.process_result_value('male', None) == UserGender.MALE
    # Teste com valor None
    assert user_gender_type.process_result_value(None, None) is None