import redis.asyncio as redis
from app.core.config import settings

_redis_client = None

async def get_redis() -> redis.Redis:
    """Get Redis connection from pool."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10,
        )
    return _redis_client

async def close_redis():
    """Close Redis connection pool."""
    global _redis_client
    if _redis_client:
        await _redis_client.aclose()
        _redis_client = None

async def set_cache(key: str, value: str, expire: int = 3600) -> None:
    """Set a value in Redis cache with expiration."""
    client = await get_redis()
    await client.setex(key, expire, value)

async def get_cache(key: str):
    """Get a value from Redis cache."""
    client = await get_redis()
    return await client.get(key)

async def delete_cache(key: str) -> None:
    """Delete a key from Redis cache."""
    client = await get_redis()
    await client.delete(key)

async def rate_limit_check(ip: str, limit: int = 60, window: int = 60) -> bool:
    """Check if an IP has exceeded rate limit. Returns True if allowed."""
    client = await get_redis()
    key = f"ratelimit:{ip}"
    count = await client.incr(key)
    if count == 1:
        await client.expire(key, window)
    return count <= limit