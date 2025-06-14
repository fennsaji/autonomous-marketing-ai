"""
Redis client for token blacklisting and session management.
"""
import logging
from typing import Optional
import redis.asyncio as redis
from app.core.config import settings

logger = logging.getLogger(__name__)

# Global Redis connection pool
redis_pool: Optional[redis.ConnectionPool] = None
redis_client: Optional[redis.Redis] = None


async def get_redis_client() -> redis.Redis:
    """
    Get Redis client instance with connection pooling.
    
    Returns:
        Redis client instance
        
    Raises:
        ConnectionError: If Redis connection fails
    """
    global redis_pool, redis_client
    
    if redis_client is None:
        try:
            redis_pool = redis.ConnectionPool.from_url(
                settings.REDIS_URL,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
                retry_on_timeout=True,
                socket_connect_timeout=settings.REDIS_CONNECT_TIMEOUT,
                socket_timeout=settings.REDIS_SOCKET_TIMEOUT
            )
            redis_client = redis.Redis(connection_pool=redis_pool)
            
            # Test connection
            await redis_client.ping()
            logger.info("Redis connection established successfully")
            
        except Exception as e:
            logger.error("Failed to connect to Redis: %s", e)
            raise ConnectionError(f"Redis connection failed: {e}") from e
    
    return redis_client


async def close_redis_connection():
    """Close Redis connection and cleanup resources."""
    global redis_pool, redis_client
    
    if redis_client:
        try:
            await redis_client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error("Error closing Redis connection: %s", e)
        finally:
            redis_client = None
            redis_pool = None


class TokenBlacklist:
    """Token blacklisting service using Redis."""
    
    def __init__(self):
        self.prefix = "blacklist:token:"
    
    async def add_token(self, token: str, ttl: int = None) -> bool:
        """
        Add token to blacklist.
        
        Args:
            token: JWT token to blacklist
            ttl: Time to live in seconds (default: from config)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            client = await get_redis_client()
            ttl = ttl or settings.TOKEN_BLACKLIST_TTL
            
            key = f"{self.prefix}{token}"
            result = await client.setex(key, ttl, "1")
            
            if result:
                logger.info("Token added to blacklist (TTL: %ds)", ttl)
                return True
            else:
                logger.error("Failed to add token to blacklist")
                return False
                
        except Exception as e:
            logger.error("Error adding token to blacklist: %s", e)
            return False
    
    async def is_blacklisted(self, token: str) -> bool:
        """
        Check if token is blacklisted.
        
        Args:
            token: JWT token to check
            
        Returns:
            True if blacklisted, False otherwise
        """
        try:
            client = await get_redis_client()
            key = f"{self.prefix}{token}"
            
            result = await client.exists(key)
            return bool(result)
            
        except Exception as e:
            logger.error("Error checking token blacklist: %s", e)
            # Fail securely - treat as not blacklisted if Redis fails
            return False
    
    async def remove_token(self, token: str) -> bool:
        """
        Remove token from blacklist (if needed for testing).
        
        Args:
            token: JWT token to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            client = await get_redis_client()
            key = f"{self.prefix}{token}"
            
            result = await client.delete(key)
            return bool(result)
            
        except Exception as e:
            logger.error("Error removing token from blacklist: %s", e)
            return False
    
    async def get_blacklist_count(self) -> int:
        """
        Get total number of blacklisted tokens.
        
        Returns:
            Number of blacklisted tokens
        """
        try:
            client = await get_redis_client()
            pattern = f"{self.prefix}*"
            
            keys = await client.keys(pattern)
            return len(keys)
            
        except Exception as e:
            logger.error("Error getting blacklist count: %s", e)
            return 0


class RateLimiter:
    """Rate limiting service using Redis."""
    
    def __init__(self):
        self.prefix = "ratelimit:"
    
    async def is_rate_limited(
        self, 
        identifier: str, 
        limit: int, 
        window: int,
        action: str = "request"
    ) -> tuple[bool, dict]:
        """
        Check if identifier is rate limited.
        
        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            limit: Maximum requests allowed
            window: Time window in seconds
            action: Action type for logging
            
        Returns:
            Tuple of (is_limited, info_dict)
        """
        try:
            client = await get_redis_client()
            key = f"{self.prefix}{action}:{identifier}"
            
            # Get current count
            current_count = await client.get(key)
            current_count = int(current_count) if current_count else 0
            
            # Check if rate limited
            if current_count >= limit:
                ttl = await client.ttl(key)
                logger.warning(
                    "Rate limit exceeded for %s: %d/%d requests (resets in %ds)",
                    identifier, current_count, limit, ttl
                )
                return True, {
                    "limited": True,
                    "current_count": current_count,
                    "limit": limit,
                    "reset_time": ttl,
                    "retry_after": ttl
                }
            
            # Increment counter
            pipe = client.pipeline()
            pipe.incr(key)
            pipe.expire(key, window)
            await pipe.execute()
            
            new_count = current_count + 1
            remaining = limit - new_count
            
            return False, {
                "limited": False,
                "current_count": new_count,
                "limit": limit,
                "remaining": remaining,
                "reset_time": window
            }
            
        except Exception as e:
            logger.error("Error checking rate limit: %s", e)
            # Fail open - don't block on Redis errors
            return False, {
                "limited": False,
                "error": str(e)
            }


# Global instances
token_blacklist = TokenBlacklist()
rate_limiter = RateLimiter()