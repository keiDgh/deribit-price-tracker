from fastapi import Depends, Request

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services import CurrencyService, PriceService

from app.infra.db.session import get_async_db

from app.infra.repositories import SqlCurrencyRepository, SqlPriceRepository

from app.infra.services import RedisClient, PriceCacheService

DBSession = Annotated[AsyncSession, Depends(get_async_db)]

def get_redis_client(request: Request):
    return RedisClient(request.app.state.redis)

RedisClientDep = Annotated[RedisClient, Depends(get_redis_client)]

def get_price_cache_service(redis_client: RedisClientDep):
    return PriceCacheService(redis_client)

PriceCacheServiceDep = Annotated[PriceCacheService, Annotated(get_price_cache_service)]

def get_currency_repository(db: DBSession):
    return SqlCurrencyRepository(db)

CurrencyRepositoryDep = Annotated[SqlCurrencyRepository, Depends(get_currency_repository)]

def get_price_repository(db: DBSession):
    return SqlPriceRepository(db)

PriceRepositoryDep = Annotated[SqlPriceRepository, Depends(get_price_repository)]

def get_currency_service(repository: CurrencyRepositoryDep):
    return CurrencyService(repository)

CurrencyServiceDep = Annotated[CurrencyService, Depends(get_currency_service)]

def get_price_service(repository: PriceRepositoryDep, price_cache_service: PriceCacheServiceDep):
    return PriceService(repository=repository, cache_service=price_cache_service)

PriceServiceDep = Annotated[PriceService, Depends(get_price_service)]
