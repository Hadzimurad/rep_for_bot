from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text 
from config import DB_URL_async
from database_module.models import Base


async_engine = create_async_engine(
    url=DB_URL_async,
    echo=False,
    # pool_size=5,
    # max_overflow=10
)

async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Создание всех таблиц в БД"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Получить сессию БД"""
    async with async_session() as session:
        yield session









