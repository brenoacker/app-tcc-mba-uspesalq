from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.user.user_repository_interface import UserRepositoryInterface
from src.usecases.user.find_user.find_user_dto import FindUserInputDto, FindUserOutputDto


class FindUserUseCase(UseCaseInterface):

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, input: FindUserInputDto) -> FindUserOutputDto:
        
        user = self.user_repository.find_user(user_id=input.user_id)

        return FindUserOutputDto(id=user.id, name=user.name, email=user.email, phone_number=user.phone_number, password=user.password)