from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.user.user_repository_interface import UserRepositoryInterface
from usecases.user.delete_user.delete_user_dto import (DeleteUserInputDto,
                                                       DeleteUserOutputDto)


class DeleteUserUseCase(UseCaseInterface):
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, input: DeleteUserInputDto) -> DeleteUserOutputDto:

        await self.user_repository.delete_user(user_id=input.id)

        return DeleteUserOutputDto()