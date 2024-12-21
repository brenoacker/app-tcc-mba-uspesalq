import uuid
from http.client import HTTPException

from domain.user.user_entity import User
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.user.add_user.add_user_dto import (AddUserInputDto,
                                                 AddUserOutputDto)


class AddUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, input: AddUserInputDto) -> AddUserOutputDto:
        
        user = User(id=uuid.uuid4(), name=input.name, email=input.email, age=input.age, gender=input.gender, phone_number=input.phone_number, password=input.password)

        user_added = self.user_repository.add_user(user=user)

        return AddUserOutputDto(id=user_added.id, name=user_added.name, email=user_added.email, age=user_added.age, gender=user_added.gender, phone_number=user_added.phone_number, password=user_added.password)