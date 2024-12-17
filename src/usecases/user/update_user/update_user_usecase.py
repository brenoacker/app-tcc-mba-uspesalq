from uuid import UUID

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.user.user_entity import User
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.user.update_user.update_user_dto import (UpdateUserInputDto,
                                                       UpdateUserOutputDto)


class UpdateUserUseCase(UseCaseInterface):

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, id: UUID, input: UpdateUserInputDto) -> UpdateUserOutputDto:
        
        user = User(id=id, name=input.name, email=input.email, phone_number=input.phone_number, password=input.password)

        self.user_repository.update_user(user=user)

        return UpdateUserOutputDto(id=id, name=user.name, email=user.email, phone_number=user.phone_number, password=user.password)