from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.user.user_entity import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def add_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def find_user(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_users(self) -> Optional[List[User]]:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        raise NotImplementedError