import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
      host=str(os.getenv("REDIS_CLIENT_URL")), 
      port=os.getenv("REDIS_PORT"),
      db=0,
      decode_responses=os.getenv("REDIS_DECODE_RESPONSES")
)

