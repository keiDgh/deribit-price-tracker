from redis.asyncio import Redis, from_url

from app.infra.settings.config import settings

async def init_redis() -> Redis:
    redis = from_url(
        settings.redis_url,          
        decode_responses=True,
        max_connections=20,         
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
    )
    await redis.ping() 
    return redis

async def close_redis(redis: Redis) -> None:
    await redis.close()