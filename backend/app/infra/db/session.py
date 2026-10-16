from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from collections.abc import Generator, AsyncGenerator
from contextlib import asynccontextmanager

from app.infra.db.engine import async_engine

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    future=True,
    expire_on_commit=False
)

# Для DI у FastAPI
def get_async_db() -> Generator[AsyncSession, None, None]:
    db = AsyncSessionLocal() 
    try:
        yield db
    finally:
        db.close()

# Для скриптов (seed, celery)
@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()