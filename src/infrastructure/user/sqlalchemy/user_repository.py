from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm.session import Session

from domain.user.user_entity import User
from domain.user.user_repository_interface import UserRepositoryInterface
from infrastructure.logging_config import logger
from infrastructure.user.sqlalchemy.user_model import UserModel


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: Session):
        self.session: Session = session

    def add_user(self, user: User) -> User:

        user_model = UserModel(id=user.id, name=user.name, email=user.email, phone_number=user.phone_number, password=user.password)

        self.session.add(user_model)
        self.session.commit()

        return User(id=user_model.id, name=user_model.name, email=user_model.email, phone_number=user_model.phone_number, password=user_model.password)

    def find_user(self, user_id: UUID) -> User:

        user_in_db: UserModel = self.session.query(UserModel).get(user_id)
        
        if not user_in_db:
            raise ValueError(f"User with id '{user_id}' not found")
        
        user = User(id=user_in_db.id, name=user_in_db.name, email=user_in_db.email, phone_number=user_in_db.phone_number, password=user_in_db.password)

        return user
    
    def find_user_by_email(self, email: str) -> Optional[User]:

        user_in_db: UserModel = self.session.query(UserModel).filter(UserModel.email == email).first()
        if not user_in_db:
            return None
       
        user = User(id=user_in_db.id, name=user_in_db.name, email=user_in_db.email, phone_number=user_in_db.phone_number, password=user_in_db.password)

        return user

    def list_users(self) -> Optional[List[User]]:

        users_in_db = self.session.query(UserModel).all()

        if not users_in_db:
            return None

        users = []
        
        for user_in_db in users_in_db:
            users.append(User(
                id=user_in_db.id, 
                name=user_in_db.name, 
                email=user_in_db.email, 
                phone_number=user_in_db.phone_number, 
                password=user_in_db.password
            ))

        for user in users:
            logger.info(f"Id: {user.id} | name: {user.name} | password: {user.password}")
        return users

    def update_user(self, user: User) -> None:

        self.session.query(UserModel).filter(UserModel.id == user.id).update(
            {
                "name": user.name,
                "email": user.email,
                "phone_number": user.phone_number,
                "password": user.password
            }
        )
        self.session.commit()

        return None
    
    def delete_user(self, user_id: UUID) -> None:
        
        self.session.query(UserModel).filter(UserModel.id == user_id).delete()
        self.session.commit()

        return None
    

