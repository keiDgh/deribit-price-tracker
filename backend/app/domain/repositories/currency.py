from app.domain.models import Currency
from abc import ABC, abstractmethod

class CurrencyRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Currency: ...

    @abstractmethod
    async def get_by_ticker(self, ticker: str) -> Currency: ...

    @abstractmethod
    async def add(ticker: str, name: str) -> Currency: ...