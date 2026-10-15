from app.domain.models import Price
from app.domain.repositories import PriceRepository

from datetime import datetime

class PriceService:
    def __init__(self, repository: PriceRepository):
        self._repository = repository

    async def get_by_id(self, id: int) -> Price:
        return await self._repository.get_by_id(id)

    async def get_by_ticker(self, ticker: str, skip: int, limit: int) -> list[Price]:
        return await self._repository.get_by_ticker(ticker)

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
            end=end
        )

    async def add(self, currency_id: int, price: float) -> Price: 
        return await self._repository.add(currency_id=currency_id, price=price)

    async def get_last(self, ticker: str) -> Price | None:
        return await self._repository.get_last(ticker)