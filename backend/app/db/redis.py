import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
    async def get(self, key: str) -> str | None:
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.warning(f"Redis GET error: {e}")
            return None
        
    async def set(self, key: str, value: str, ttl: int = None):
        try:
            ttl = ttl or settings.REDIS_TTL_SECONDS
            await self.redis.set(key, value, ex=ttl)
        except Exception as e:
            logger.warning(f"Redis SET error: {e}")
            
    async def close(self):
        await self.redis.close()
        
cache = RedisCache()