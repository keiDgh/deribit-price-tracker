from sqlalchemy.ext.asyncio import create_async_engine

from app.infra.settings.config import settings

async_engine = create_async_engine(
    settings.database_url, 
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
    future=True,
)