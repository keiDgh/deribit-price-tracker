from abc import ABC, abstractmethod

from app.domain.models import Price

class PriceCachePort(ABC):
    """Порт кэш-сервиса для работы с последней ценой валюты"""
    @abstractmethod
    async def get(self, ticker: str) -> Price: ...

    @abstractmethod
    async def set(self, ticker: str, price: Price) -> None: ...