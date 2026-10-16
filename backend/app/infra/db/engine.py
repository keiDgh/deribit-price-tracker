from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from app.infra.settings.config import settings

async_engine = create_async_engine(
    settings.database_url,
    poolclass=NullPool,
    future=True,
)