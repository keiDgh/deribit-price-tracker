from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.repositories import CurrencyRepository
from app.domain.models import Currency
from app.domain.exceptions import CurrencyNotFoundError

from app.infra.db.models import Currency as CurrencyORM

class SqlCurrencyRepository(CurrencyRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    def _to_domain(self, currency: CurrencyORM) -> Currency:
        return Currency(
            id=currency.id, 
            ticker=currency.ticker, 
            name=currency.name
        )

    async def get_by_id(self, id: int) -> Currency:
        query = (
            select(CurrencyORM).
            options(selectinload(CurrencyORM.prices)).
            where(CurrencyORM.id==id)
        )
        currency = (await self._db.execute(query)).scalars().first()

        if currency is None:
            raise CurrencyNotFoundError(f"Currency with ID {id} was not found")

        return self._to_domain(currency)

    async def get_by_ticker(self, ticker: str) -> Currency:
        query = (
            select(CurrencyORM).
            options(selectinload(CurrencyORM.prices)).
            where(CurrencyORM.ticker==ticker)        
        )
        currency = (await self._db.execute(query)).scalars().first()

        if currency is None:
            raise CurrencyNotFoundError(f"Currency with ticker {ticker} was not found")

        return self._to_domain(currency)

    async def get_all(self):
        query = select(CurrencyORM)
        currencies = (await self._db.execute(query)).scalars().all()

        return [self._to_domain(currency) for currency in currencies]
        

    
        