# test_cache.py
import asyncio
from app.db.redis import cache

async def test():
    await cache.set("test:key", "Hello Redis!", ttl=10)
    value = await cache.get("test:key")
    print(value)  # Hello Redis!

    await cache.close()

asyncio.run(test())