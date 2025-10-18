"""Cache factory for creating cache instances."""
from typing import Optional
from .base_cache import ICache
from .memory_cache import MemoryCache
from .redis_cache import RedisCache


def create_cache(
    cache_type: str = "memory",
    max_size: int = 1000,
    default_ttl: int = 3600,
    redis_host: str = "localhost",
    redis_port: int = 6379,
    redis_db: int = 0,
    redis_password: Optional[str] = None,
) -> ICache:
    """
    Factory function to create cache instance.
    
    Args:
        cache_type: Type of cache ("memory" or "redis")
        max_size: Maximum size for memory cache
        default_ttl: Default TTL in seconds
        redis_host: Redis host (if using redis)
        redis_port: Redis port (if using redis)
        redis_db: Redis database (if using redis)
        redis_password: Redis password (if using redis)
        
    Returns:
        Cache instance
        
    Raises:
        ValueError: If cache_type is invalid
    """
    if cache_type == "memory":
        return MemoryCache(max_size=max_size, default_ttl=default_ttl)
    elif cache_type == "redis":
        return RedisCache(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            default_ttl=default_ttl,
        )
    else:
        raise ValueError(f"Invalid cache type: {cache_type}. Use 'memory' or 'redis'")
