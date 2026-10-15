from fastapi import Depends

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services import CurrencyService, PriceService

from app.infra.db.session import get_async_db

from app.infra.repositories import SqlCurrencyRepository, SqlPriceRepository

DBSession = Annotated[AsyncSession, Depends(get_async_db)]

def get_currency_repository(db: DBSession):
    return SqlCurrencyRepository(db)

CurrencyRepositoryDep = Annotated[SqlCurrencyRepository, Depends(get_currency_repository)]

def get_price_repository(db: DBSession):
    return SqlPriceRepository(db)

PriceRepositoryDep = Annotated[SqlPriceRepository, Depends(get_price_repository)]

def get_currency_service(repository: CurrencyRepositoryDep):
    return CurrencyService(repository)

CurrencyServiceDep = Annotated[CurrencyService, Depends(get_currency_service)]

def get_currency_service(repository: PriceRepositoryDep):
    return PriceService(repository)

PriceServiceDep = Annotated[PriceService, Depends(get_currency_service)]



