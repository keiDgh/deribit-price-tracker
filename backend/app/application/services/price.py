from app.domain.models import Price
from app.domain.repositories import PriceRepository

from app.application.ports import PriceCachePort
from app.application.exceptions import CacheError

from datetime import datetime
from decimal import Decimal

class PriceService:
    def __init__(self, repository: PriceRepository, cache_service: PriceCachePort):
        self._repository=repository
        self._cache=cache_service

    async def get_by_id(self, id: int) -> Price:
        return await self._repository.get_by_id(id)

    async def get_by_ticker(self, ticker: str, skip: int, limit: int) -> list[Price]:
        return await self._repository.get_by_ticker(ticker=ticker, skip=skip, limit=limit)

    async def get_by_ticker_and_period(
            self, 
            ticker: str, 
            start: datetime, 
            end: datetime, 
            skip: int, 
            limit: int
    ) -> list[Price]: 
        return await self._repository.get_by_ticker_and_period(
            ticker=ticker, 
            start=start, 
            end=end, 
            skip=skip, 
            limit=limit
        )

    async def add(self, currency_id: int, price: Decimal, timestamp: int) -> Price: 
        return await self._repository.add(currency_id=currency_id, price=price, timestamp=timestamp)

    async def get_last(self, ticker: str) -> Price | None:
        try:
            cached = await self._cache.get(ticker) 
        except CacheError:
            return await self._repository.get_last(ticker)

        if cached is not None:
            return cached

        price = await self._repository.get_last(ticker)
        if price is not None:
            try:
                await self._cache.set(ticker=ticker, price=price)
            except CacheError:
                pass
            
        return price