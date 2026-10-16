from redis.asyncio import Redis, ConnectionError, TimeoutError

from app.application.exceptions import RedisError

class RedisClient:
    def __init__(self, redis: Redis):
        self._redis=redis

    async def get(self, id: str) -> str | None:
        try:
            result = await self._redis.get(id)
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Could not connect to redis") from e

        return result

    async def set(self, id: str, value: str, ex: int | None = None) -> None:
        try:
            await self._redis.set(id, value, ex=ex)
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Could not connect to redis") from e

    async def delete(self, id: str) -> None:
        try:
            await self._redis.delete(id)
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Could not connect to redis") from e