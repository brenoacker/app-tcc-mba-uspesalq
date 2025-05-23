from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.user.find_user.find_user_dto import (FindUserInputDto,
                                                   FindUserOutputDto)


class FindUserUseCase(UseCaseInterface):

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, input: FindUserInputDto) -> FindUserOutputDto:
        
        user = await self.user_repository.find_user(user_id=input.id)

        if user is None:
            raise ValueError(f"User with id '{input.id}' not found")

        return FindUserOutputDto(id=user.id, name=user.name, email=user.email, age=user.age, gender=user.gender, phone_number=user.phone_number, password=user.password)