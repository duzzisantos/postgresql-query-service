from redis_caching.redis_connection import redis_client
import json

async def manage_caching(key: str, ttl: int, data):
    cached = await redis_client.get(key)
    if cached:
        return json.loads(cached)
    

    await redis_client.setex(key, ttl, json.dumps(data))
    return data
