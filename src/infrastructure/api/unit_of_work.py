from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from .database import SessionLocal

T = TypeVar('T')

class AsyncUnitOfWork:
    """
    Implementação assíncrona do padrão Unit of Work para gerenciar transações.
    
    Permite agrupar múltiplas operações de banco de dados em uma única transação,
    com commit automático em caso de sucesso e rollback em caso de exceção.
    """
    
    def __init__(self):
        self.session: AsyncSession = None
    
    async def __aenter__(self) -> 'AsyncUnitOfWork':
        self.session = SessionLocal()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()
    
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()


@asynccontextmanager
async def get_uow() -> AsyncGenerator[AsyncUnitOfWork, None]:
    """
    Context manager para obter uma instância do Unit of Work.
    
    Exemplo de uso:
    ```
    async with get_uow() as uow:
        # Executar operações de banco de dados
        result = await some_repository(uow.session).find_by_id(id)
        await uow.commit()  # Opcional, pois o commit é automático ao sair do contexto sem exceções
    ```
    """
    async with AsyncUnitOfWork() as uow:
        yield uow


async def run_in_transaction(
    func: Callable[[AsyncSession], T]
) -> T:
    """
    Executa uma função dentro de uma transação com commit/rollback automático.
    
    Exemplo de uso:
    ```
    result = await run_in_transaction(
        lambda session: some_repository(session).find_by_id(id)
    )
    ```
    """
    async with AsyncUnitOfWork() as uow:
        result = await func(uow.session)
        return result