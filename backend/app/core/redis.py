"""
Redis configuration and connection management.
"""
import redis

from app.core.config import settings

# Create Redis connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis():
    """Get Redis client."""
    return redis_client


def test_redis_connection():
    """Test Redis connection."""
    try:
        redis_client.ping()
        return True
    except Exception:
        return False