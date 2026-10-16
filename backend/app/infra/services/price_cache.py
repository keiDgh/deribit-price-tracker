from app.application.ports import PriceCachePort
from app.application.exceptions import CacheInvalidError

from app.domain.models import Price

from app.infra.settings.config import settings
from app.infra.services import RedisClient

import json
from datetime import datetime
from decimal import Decimal

class PriceCacheService(PriceCachePort):
    def __init__(self, redis: RedisClient):
        self._redis=redis
        self._ttl=settings.cache_ttl_seconds

    def _serialize(self, value: Price) -> str:
        result = {
            "id": value.id, 
            "currency_id": value.currency_id, 
            "price": str(value.price), 
            "timestamp": value.timestamp, 
            "created_at": str(value.created_at)
        }
        return json.dumps(result)

    def _deserialize(self, value: str | None) -> Price:
        if value is None:
            return None
        
        try:
            loaded = json.loads(value)
            result = Price(
                id=int(loaded["id"]), 
                currency_id=int(loaded["currency_id"]), 
                price=Decimal(loaded["price"]), 
                timestamp=int(loaded["timestamp"]), 
                created_at=datetime.fromisoformat(loaded["created_at"])
            )
        except (KeyError, ValueError, TypeError, json.JSONDecodeError) as e:
            raise CacheInvalidError("Cache is not valid") from e
        return result

    async def get(self, ticker: str) -> Price:
        result = await self._redis.get(ticker)

        try:
            value = self._deserialize(result)
        except CacheInvalidError:
            await self._redis.delete(ticker)
        
        return value

    async def set(self, ticker: str, price: Price) -> None: 
        value = self._serialize(price)

        await self._redis.set(id=ticker, value=value, ex=self._ttl)