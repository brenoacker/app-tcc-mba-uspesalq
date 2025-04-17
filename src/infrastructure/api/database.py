from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Criação do AsyncEngine com o driver asyncpg
engine = create_async_engine("postgresql+asyncpg://postgres:postgres@postgres/db", echo=True, future=True)

# Configuração do AsyncSession
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

# Função para obter uma sessão assíncrona
async def get_session():
    async with SessionLocal() as session:
        yield session

# Função para criar tabelas de forma assíncrona
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)