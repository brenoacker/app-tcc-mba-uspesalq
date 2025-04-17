from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.user.user_entity import User
from domain.user.user_repository_interface import UserRepositoryInterface
from infrastructure.logging_config import logger
from infrastructure.user.sqlalchemy.user_model import UserModel


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_user(self, user: User) -> User:

        user_model = UserModel(id=user.id, name=user.name, email=user.email, age=user.age, gender=user.gender, phone_number=user.phone_number, password=user.password)

        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)

        return User(id=user_model.id, name=user_model.name, email=user_model.email, age=user_model.age, gender=user_model.gender, phone_number=user_model.phone_number, password=user_model.password)

    async def find_user(self, user_id: UUID) -> User:

        result = await self.session.execute(select(UserModel).filter(UserModel.id == user_id))
        user_in_db = result.scalars().first()
        
        if not user_in_db:
            raise ValueError(f"User with id '{user_id}' not found")
        
        user = User(id=user_in_db.id, name=user_in_db.name, email=user_in_db.email, age=user_in_db.age, gender=user_in_db.gender, phone_number=user_in_db.phone_number, password=user_in_db.password)

        return user
    
    async def find_user_by_email(self, email: str) -> Optional[User]:

        result = await self.session.execute(select(UserModel).filter(UserModel.email == email))
        user_in_db = result.scalars().first()
        
        if not user_in_db:
            return None
       
        user = User(id=user_in_db.id, name=user_in_db.name, email=user_in_db.email, age=user_in_db.age, gender=user_in_db.gender, phone_number=user_in_db.phone_number, password=user_in_db.password)

        return user

    async def list_users(self) -> Optional[List[User]]:

        result = await self.session.execute(select(UserModel))
        users_in_db = result.scalars().all()

        if not users_in_db:
            return None

        users = []
        
        for user_in_db in users_in_db:
            users.append(User(
                id=user_in_db.id, 
                name=user_in_db.name, 
                email=user_in_db.email, 
                age=user_in_db.age,
                gender=user_in_db.gender,
                phone_number=user_in_db.phone_number, 
                password=user_in_db.password
            ))

        return users

    async def update_user(self, user: User) -> None:

        stmt = select(UserModel).filter(UserModel.id == user.id)
        result = await self.session.execute(stmt)
        user_model = result.scalars().first()
        
        if user_model:
            user_model.name = user.name
            user_model.email = user.email
            user_model.age = user.age
            user_model.gender = user.gender
            user_model.phone_number = user.phone_number
            user_model.password = user.password
            await self.session.commit()

        return None
    
    async def delete_user(self, user_id: UUID) -> None:
        
        stmt = select(UserModel).filter(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user_model = result.scalars().first()
        
        if user_model:
            await self.session.delete(user_model)
            await self.session.commit()

        return None
    

