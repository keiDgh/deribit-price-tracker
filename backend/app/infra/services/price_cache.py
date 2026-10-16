from app.application.ports import PriceCachePort
from app.application.exceptions import CacheInvalidError

from app.domain.models import Price

from app.infra.settings.config import settings
from app.infra.services import RedisClient

import json
from dataclasses import fields

class PriceCacheService(PriceCachePort):
    def __init__(self, redis: RedisClient):
        self._redis=redis
        self._ttl=settings.cache_ttl_seconds

    def _serialize(self, value: Price) -> str:
        result = json.dumps({c.name: getattr(value, c.name) for c in fields(value)})
        return result

    def _deserialize(self, value: str | None) -> Price:
        if value is None:
            return None
        
        try:
            loaded = json.loads(value)
            result = Price(**loaded)
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            raise CacheInvalidError("Cache is not valid") from e
        return result

    async def get(self, ticker: str) -> Price:
        result = await self._redis.get(ticker)

        try:
            value = self._deserialize(result)
        except CacheInvalidError:
            await self._redis.delete(ticker)
        
        return value

    async def set(self, ticker: str, value: Price) -> None: 
        value = self._serialize(value)

        await self._redis.set(id=ticker, value=value, ex=self._ttl)