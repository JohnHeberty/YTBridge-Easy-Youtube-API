"""Abstract cache interface."""
from abc import ABC, abstractmethod
from typing import Any, Optional


class ICache(ABC):
    """Abstract cache interface following Interface Segregation Principle."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache by key."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set value in cache with optional TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache by key."""
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """Clear all cache."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass
