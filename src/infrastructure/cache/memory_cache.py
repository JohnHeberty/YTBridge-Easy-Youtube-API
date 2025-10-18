"""In-memory cache implementation."""
import asyncio
import time
from typing import Any, Optional, Dict
from collections import OrderedDict
from .base_cache import ICache


class MemoryCache(ICache):
    """
    In-memory cache implementation using OrderedDict for LRU behavior.
    Thread-safe using asyncio locks.
    """

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        Initialize memory cache.
        
        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default time to live in seconds
        """
        self._cache: OrderedDict[str, tuple[Any, Optional[float]]] = OrderedDict()
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache by key."""
        async with self._lock:
            if key not in self._cache:
                return None

            value, expiry = self._cache[key]

            # Check if expired
            if expiry is not None and time.time() > expiry:
                del self._cache[key]
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        async with self._lock:
            # Calculate expiry time
            expiry = None
            if ttl is not None:
                expiry = time.time() + ttl
            elif self._default_ttl > 0:
                expiry = time.time() + self._default_ttl

            # Remove oldest item if cache is full
            if key not in self._cache and len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)

            # Add/update item
            self._cache[key] = (value, expiry)
            self._cache.move_to_end(key)

            return True

    async def delete(self, key: str) -> bool:
        """Delete value from cache by key."""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    async def clear(self) -> bool:
        """Clear all cache."""
        async with self._lock:
            self._cache.clear()
            return True

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        async with self._lock:
            if key not in self._cache:
                return False

            value, expiry = self._cache[key]

            # Check if expired
            if expiry is not None and time.time() > expiry:
                del self._cache[key]
                return False

            return True

    async def cleanup_expired(self):
        """Remove expired items from cache."""
        async with self._lock:
            current_time = time.time()
            expired_keys = [
                key
                for key, (_, expiry) in self._cache.items()
                if expiry is not None and current_time > expiry
            ]

            for key in expired_keys:
                del self._cache[key]

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "default_ttl": self._default_ttl,
        }
