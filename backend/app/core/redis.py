"""
Redis configuration and connection management.
"""
import redis.asyncio as redis
from app.core.config import settings


class RedisManager:
    """Redis connection manager."""
    
    def __init__(self):
        self.redis_client = None
    
    async def connect(self):
        """Connect to Redis."""
        self.redis_client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        return self.redis_client
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis_client:
            await self.redis_client.close()
    
    async def get_client(self):
        """Get Redis client instance."""
        if not self.redis_client:
            await self.connect()
        return self.redis_client


# Global Redis manager instance
redis_manager = RedisManager()


async def get_redis():
    """Dependency to get Redis client."""
    return await redis_manager.get_client()