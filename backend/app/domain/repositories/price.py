from app.domain.models import Price
from abc import ABC, abstractmethod

from decimal import Decimal
from datetime import datetime

class PriceRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Price: ...

    @abstractmethod
    async def get_by_ticker(self, ticker: str, skip: int, limit: int) -> list[Price]: ...

    @abstractmethod
    async def get_by_ticker_and_period(self, ticker: str, start: datetime, end: datetime, skip: int, limit: int) -> list[Price]: ...

    @abstractmethod
    async def get_last(self, ticker: str) -> Price | None: ...

    @abstractmethod
    async def add(self, currency_id: int, price: Decimal, timestamp: int) -> Price: ...