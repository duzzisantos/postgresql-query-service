from upstash_redis import Redis
import json
from app.core.config import settings


async def manage_caching(key: str, ttl: int, fetch_fn):

    try:
        redis = Redis(
            url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_TOKEN
        )
        cached = redis.get(key)
        if cached:
            return json.loads(cached)
    except Exception:
        pass

    # Cache miss — execute the actual query
    if callable(fetch_fn):
        data = await fetch_fn()
    else:
        data = fetch_fn

    try:
        redis = Redis(
            url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_TOKEN
        )
        redis.setex(key, ttl, json.dumps(data, default=str))
    except Exception:
        pass

    return data


async def invalidate_cache(pattern: str):
    """Delete cache keys matching a pattern after mutations."""
    try:
        redis = Redis(
            url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_TOKEN
        )
        for key in redis.scan(match=pattern):
            redis.delete(key)
    except Exception:
        pass
