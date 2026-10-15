from collections.abc import Generator

from sqlalchemy.orm import Session

from app.infra.db.engine import async_engine

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    autocommit=False,
    future=True,
    expire_on_commit=False
)

def get_async_db() -> Generator[AsyncSession, None, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()