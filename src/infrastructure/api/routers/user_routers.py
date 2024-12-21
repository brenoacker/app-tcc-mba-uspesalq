import traceback
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.api.database import get_session
from infrastructure.user.sqlalchemy.user_repository import UserRepository
from usecases.user.add_user.add_user_dto import AddUserInputDto
from usecases.user.add_user.add_user_usecase import AddUserUseCase
from usecases.user.find_user.find_user_dto import FindUserInputDto
from usecases.user.find_user.find_user_usecase import FindUserUseCase
from usecases.user.list_users.list_users_dto import ListUsersInputDto
from usecases.user.list_users.list_users_usecase import ListUsersUseCase
from usecases.user.update_user.update_user_dto import UpdateUserInputDto
from usecases.user.update_user.update_user_usecase import UpdateUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=201)
def add_user(request: AddUserInputDto, session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        find_user_by_email = user_repository.find_user_by_email(email=request.email)
        if find_user_by_email:
            raise HTTPException(status_code=422, detail=f"Email '{request.email}' already registered")
        usecase = AddUserUseCase(user_repository=user_repository)
        output = usecase.execute(input=request)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/{user_id}")
def find_user(user_id: UUID, session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        usecase = FindUserUseCase(user_repository=user_repository)
        output = usecase.execute(input=FindUserInputDto(id=user_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found") from e

@router.get("/")
def list_users(session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        usecase = ListUsersUseCase(user_repository=user_repository)
        output = usecase.execute()
        user_ids = [user.id for user in output.users]
        # crie um arquivo que contenha os ids dos usuários, cada um em uma linha
        with open("user_ids.txt", "w") as f:
            for user_id in user_ids:
                f.write(f"{user_id}\n")

        return output

    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e  
    
@router.patch("/{user_id}")
def update_user(user_id: UUID, request: UpdateUserInputDto, session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        user_found = user_repository.find_user(user_id=user_id)
        
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user_found, key, value)

        usecase = UpdateUserUseCase(user_repository=user_repository)
        output = usecase.execute(
            id=user_id,
            input=UpdateUserInputDto(
                name=user_found.name,
                email=user_found.email,
                phone_number=user_found.phone_number,
                password=user_found.password
            )
        )
        return output
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        user_repository.find_user(user_id=user_id)

        user_repository.delete_user(user_id=user_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    