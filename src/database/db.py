from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker)
from sqlmodel import SQLModel, create_engine

from src.core.config.env_data import Config

# create async engine
async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))


# database connection initialization
async def db_init():
    async with async_engine.begin() as conn:
        # from src.user_module.model import User

        await conn.run_sync(SQLModel.metadata.create_all)


# create async session
async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


# get the async session
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
