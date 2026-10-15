from app.domain.models import Currency
from app.domain.repositories import CurrencyRepository

class CurrencyService:
    def __init__(self, repository: CurrencyRepository):
        self._repository = repository

    async def get_by_id(self, id: int) -> Currency:
        return await self._repository.get_by_id(id)

    async def get_by_ticker(self, ticker: str) -> Currency:
        return await self._repository.get_by_ticker(ticker)    

    async def get_all(self) -> list[Currency]:
        return await self._repository.get_all()