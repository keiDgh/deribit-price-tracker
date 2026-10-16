from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

from datetime import datetime
from decimal import Decimal

from app.domain.repositories import PriceRepository
from app.domain.models import Price
from app.domain.exceptions import PriceNotFoundError, RelatedCurrencyNotFound, DuplicatePriceError

from app.infra.db.models import Price as PriceORM, Currency as CurrencyORM

class SqlPriceRepository(PriceRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    def _to_domain(self, price: PriceORM) -> Price:
        return Price(
            id=price.id, 
            currency_id=price.currency_id, 
            price=price.price, 
            timestamp=price.timestamp, 
            created_at=price.created_at
        )

    async def get_by_id(self, id: int) -> Price:
        query = (
            select(PriceORM).
            options(selectinload(PriceORM.currency)).
            where(PriceORM.id==id)
        )
        price = (await self._db.execute(query)).scalars().first()

        if price is None: 
            raise PriceNotFoundError(f"Price with ID {id} was not found")

        return self._to_domain(price)

    async def get_by_ticker(self, ticker: str, skip: int, limit: int) -> list[Price]:
        query = (
            select(PriceORM)
            .join(CurrencyORM, PriceORM.currency_id == CurrencyORM.id)
            .where(CurrencyORM.ticker == ticker)
            .order_by(PriceORM.timestamp.asc()).
            offset(skip).
            limit(limit)
        )
        prices = (await self._db.execute(query)).scalars().all()
        
        return  [self._to_domain(price) for price in prices]

    async def get_by_ticker_and_period(
            self, 
            ticker: str, 
            start: datetime, 
            end: datetime, 
            skip: int, 
            limit: int
    ) -> list[Price]: 
        query = (
            select(PriceORM)
            .join(CurrencyORM, PriceORM.currency_id == CurrencyORM.id)
            .where(
                CurrencyORM.ticker == ticker,
                PriceORM.timestamp >= start,
                PriceORM.timestamp <= end,
            )
            .order_by(PriceORM.timestamp.asc()).
            offset(skip).
            limit(limit)
        )
        prices = (await self._db.execute(query)).scalars().all()

        return [self._to_domain(price) for price in prices]

    async def add(
            self, 
            currency_id: int, 
            price: Decimal, 
            timestamp: int
    ) -> Price: 

        price = PriceORM(currency_id=currency_id, price=price, timestamp=timestamp)

        self._db.add(price)
        try:
            await self._db.commit()
        except ForeignKeyViolationError:
            await self._db.rollback()
            raise RelatedCurrencyNotFound(f"Currency with ID {currency_id} does not exist. ForeignKey violation")
        except UniqueViolationError:
            await self._db.rollback()
            raise DuplicatePriceError(f"Price with {currency_id} and {timestamp} already exists")
        
        await self._db.refresh(price)

        return self._to_domain(price)

    async def get_last(self, ticker: str) -> Price | None:
        query = (
            select(PriceORM)
            .join(CurrencyORM, PriceORM.currency_id == CurrencyORM.id)
            .where(CurrencyORM.ticker == ticker)
            .order_by(desc(PriceORM.timestamp)).
            limit(1)
        )
        price = (await self._db.execute(query)).scalars().first()

        if price is None:
            return 

        return self._to_domain(price)