from sqlalchemy import Column, Integer, String, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID

from domain.user.user_gender_enum import UserGender
from infrastructure.api.database import Base


class UserGenderType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, UserGender):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return UserGender(value)
        return value

class UserModel(Base):
    __tablename__ = "tb_users"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(UserGenderType)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
