from app.redis_caching.redis_connection import get_redis_client
import json


async def manage_caching(key: str, ttl: int, fetch_fn):
    """
    Check cache first; on miss, call fetch_fn (an async callable),
    cache the result, and return it.
    """
    try:
        client = get_redis_client()
        cached = await client.get(key)
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
        client = get_redis_client()
        await client.setex(key, ttl, json.dumps(data, default=str))
    except Exception:
        pass

    return data


async def invalidate_cache(pattern: str):
    """Delete cache keys matching a pattern after mutations."""
    try:
        client = get_redis_client()
        async for key in client.scan_iter(match=pattern):
            await client.delete(key)
    except Exception:
        pass
