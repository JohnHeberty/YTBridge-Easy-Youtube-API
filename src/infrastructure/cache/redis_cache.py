"""Redis cache implementation."""
import json
from typing import Any, Optional
from .base_cache import ICache

try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class RedisCache(ICache):
    """
    Redis cache implementation.
    Requires redis package: pip install redis
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        default_ttl: int = 3600,
    ):
        """
        Initialize Redis cache.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password
            default_ttl: Default time to live in seconds
        """
        if not REDIS_AVAILABLE:
            raise ImportError(
                "redis package is required for RedisCache. "
                "Install it with: pip install redis"
            )

        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._default_ttl = default_ttl
        self._redis: Optional[aioredis.Redis] = None

    async def _get_client(self) -> aioredis.Redis:
        """Get or create Redis client."""
        if self._redis is None:
            self._redis = await aioredis.from_url(
                f"redis://{self._host}:{self._port}/{self._db}",
                password=self._password,
                encoding="utf-8",
                decode_responses=True,
            )
        return self._redis

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache by key."""
        client = await self._get_client()
        value = await client.get(key)

        if value is None:
            return None

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        client = await self._get_client()
        ttl_to_use = ttl if ttl is not None else self._default_ttl

        # Serialize value to JSON
        try:
            serialized_value = json.dumps(value)
        except (TypeError, ValueError):
            serialized_value = str(value)

        if ttl_to_use > 0:
            await client.setex(key, ttl_to_use, serialized_value)
        else:
            await client.set(key, serialized_value)

        return True

    async def delete(self, key: str) -> bool:
        """Delete value from cache by key."""
        client = await self._get_client()
        result = await client.delete(key)
        return result > 0

    async def clear(self) -> bool:
        """Clear all cache."""
        client = await self._get_client()
        await client.flushdb()
        return True

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        client = await self._get_client()
        result = await client.exists(key)
        return result > 0

    async def close(self):
        """Close Redis connection."""
        if self._redis is not None:
            await self._redis.close()
            self._redis = None
