import redis.asyncio as aioredis
from app.core.config import settings

_client = None


def get_redis_client():
    global _client
    if _client is None:
        _client = aioredis.Redis(
            host=settings.REDIS_CLIENT_URL,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=settings.REDIS_DECODE_RESPONSES,
        )
    return _client
