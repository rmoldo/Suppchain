import os

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker



SQLALCHAMY_DATABASE_URL = "postgresql+asyncpg://radu:raduadu@postgres:5432/ecomm_db"

engine = create_async_engine(SQLALCHAMY_DATABASE_URL, echo=True, future=True)



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session