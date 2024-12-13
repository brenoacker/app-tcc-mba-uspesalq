from src.domain.__seedwork.use_case_interface import UseCaseInterface
from src.domain.user.user_entity import User
from src.domain.user.user_repository_interface import UserRepositoryInterface
from src.usecases.user.update_user.update_user_dto import UpdateUserInputDto, UpdateUserOutputDto


class UpdateUserUseCase(UseCaseInterface):

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, input: UpdateUserInputDto) -> UpdateUserOutputDto:
        
        user = User(id=input.user_id, name=input.name, email=input.email, phone_number=input.phone_number, password=input.password)

        self.user_repository.update_user(user=user)

        return UpdateUserOutputDto(id=user.id, name=user.name, email=user.email, phone_number=user.phone_number, password=user.password)