from typing import Optional

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.user.list_users.list_users_dto import (ListUsersOutputDto,
                                                     UserDto)


class ListUsersUseCase(UseCaseInterface):

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self) -> Optional[ListUsersOutputDto]:

        users = self.user_repository.list_users()

        if not users:
            return ListUsersOutputDto(users=[])

        users_dto = [UserDto(id=user.id, name=user.name, email=user.email, age=user.age, gender=user.gender, phone_number=user.phone_number, password=user.password) for user in users]
        
        return ListUsersOutputDto(users=users_dto)