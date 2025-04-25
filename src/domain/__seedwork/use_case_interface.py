from abc import ABC, abstractmethod
from typing import Any


class UseCaseInterface(ABC):

    @abstractmethod
    async def execute(self, input: Any) -> Any:
        raise NotImplementedError
