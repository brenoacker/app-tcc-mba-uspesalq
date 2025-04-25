from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Criação do AsyncEngine com o driver asyncpg
# Ajustando pool_size, max_overflow e pool_timeout para otimizar o throughput
engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@postgres/db", 
    echo=False,                # Desativando logs para melhorar performance
    future=True,
    pool_size=40,              # Aumentando o tamanho do pool para maior throughput
    max_overflow=60,           # Permitindo mais conexões temporárias
    pool_timeout=10,           # Reduzindo o timeout para falhar mais rápido
    pool_pre_ping=True,        # Verifica se a conexão está ativa antes de usá-la
    pool_recycle=1800,         # Recicla conexões a cada 30 minutos
    pool_use_lifo=True,        # Usa LIFO para melhor reutilização de conexões quentes
    connect_args={             # Argumentos específicos para o asyncpg
        "statement_cache_size": 0,  # Desabilita cache para evitar memory leaks
        "prepared_statement_cache_size": 100,  # Limite de statements preparados
        "command_timeout": 10        # Timeout para comandos em segundos
    }
)

# Configuração do AsyncSession
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,   # Evita consultas extras após commit
)

# Use the imported declarative_base from sqlalchemy.orm
Base = declarative_base()

# Função para obter uma sessão assíncrona
async def get_session():
    async with SessionLocal() as session:
        yield session

# Função para criar tabelas de forma assíncrona
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Função para alterar colunas específicas para permitir valores nulos
async def alter_payment_columns():
    async with engine.begin() as conn:
        # Alterando as colunas payment_method e payment_card_gateway para aceitar NULL
        await conn.execute(text("ALTER TABLE tb_payments ALTER COLUMN payment_method DROP NOT NULL"))
        await conn.execute(text("ALTER TABLE tb_payments ALTER COLUMN payment_card_gateway DROP NOT NULL"))
        print("Colunas payment_method e payment_card_gateway alteradas para aceitar NULL")
