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
        
        user = User(id=uuid.uuid4(), name=input.name, email=input.email, phone_number=input.phone_number, password=input.password)

        self.user_repository.add_user(user=user)

        return AddUserOutputDto(id=user.id, name=user.name, email=user.email, phone_number=user.phone_number, password=user.password)