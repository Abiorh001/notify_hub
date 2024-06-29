from sqlmodel import create_engine, SQLModel
from core.config.env_data import Config
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


# create async engine
async_engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
        )
)


# database connection initialization
async def db_init():
    async with async_engine.begin() as conn:
        from user.model import User
        await conn.run_sync(SQLModel.metadata.create_all)

# create async session
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# get the async session
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session