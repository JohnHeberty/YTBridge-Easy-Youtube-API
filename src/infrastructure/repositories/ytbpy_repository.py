"""YouTube repository implementation using ytbpy module."""
import asyncio
import hashlib
import json
from typing import Dict, Any, Optional
from src.domain.repositories import IYouTubeRepository
from src.infrastructure.cache import ICache
from src.infrastructure.ytbpy import channel, playlist, video, search


class YTBPyRepository(IYouTubeRepository):
    """
    Concrete implementation of YouTube repository using ytbpy module.
    Includes caching layer to reduce YouTube requests.
    """

    def __init__(self, cache: Optional[ICache] = None):
        """
        Initialize repository with optional cache.
        
        Args:
            cache: Cache implementation (optional)
        """
        self._cache = cache

    def _generate_cache_key(self, prefix: str, **kwargs) -> str:
        """
        Generate a cache key from parameters.
        
        Args:
            prefix: Key prefix
            **kwargs: Parameters to include in key
            
        Returns:
            Cache key string
        """
        # Sort kwargs for consistent key generation
        sorted_params = json.dumps(kwargs, sort_keys=True)
        param_hash = hashlib.md5(sorted_params.encode()).hexdigest()[:8]
        return f"{prefix}:{param_hash}"

    async def _get_cached_or_fetch(
        self, cache_key: str, fetch_func, ttl: Optional[int] = None
    ) -> Any:
        """
        Get data from cache or fetch and cache it.
        
        Args:
            cache_key: Cache key
            fetch_func: Function to fetch data if not cached
            ttl: Time to live for cache entry
            
        Returns:
            Cached or fetched data
        """
        # Try to get from cache
        if self._cache is not None:
            cached_data = await self._cache.get(cache_key)
            if cached_data is not None:
                return cached_data

        # Fetch data in thread pool (ytbpy is synchronous)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, fetch_func)

        # Cache the result
        if self._cache is not None and data is not None:
            await self._cache.set(cache_key, data, ttl)

        return data

    async def get_channel_info(
        self,
        channel_input: str,
        include_videos: bool = True,
        max_videos: int = 10,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        """Get detailed information about a YouTube channel."""
        cache_key = self._generate_cache_key(
            "channel_info",
            channel=channel_input,
            videos=include_videos,
            max=max_videos,
        )

        return await self._get_cached_or_fetch(
            cache_key,
            lambda: channel.get_channel_info(
                channel_input, include_videos, max_videos, timeout
            ),
        )

    async def get_channel_videos(
        self, channel_input: str, max_results: int = 50, timeout: int = 10
    ) -> Dict[str, Any]:
        """Get videos from a YouTube channel."""
        cache_key = self._generate_cache_key(
            "channel_videos", channel=channel_input, max=max_results
        )

        return await self._get_cached_or_fetch(
            cache_key,
            lambda: channel.get_channel_videos(channel_input, max_results, timeout),
        )

    async def get_playlist_info(
        self, url_or_id: str, max_results: int = 50, timeout: int = 10
    ) -> Dict[str, Any]:
        """Get information about a YouTube playlist."""
        cache_key = self._generate_cache_key(
            "playlist_info", playlist=url_or_id, max=max_results
        )

        return await self._get_cached_or_fetch(
            cache_key,
            lambda: playlist.get_playlist_info(url_or_id, max_results, timeout),
        )

    async def get_video_info(self, url_or_id: str, timeout: int = 10) -> Dict[str, Any]:
        """Get detailed information about a YouTube video."""
        cache_key = self._generate_cache_key("video_info", video=url_or_id)

        return await self._get_cached_or_fetch(
            cache_key, lambda: video.get_video_info(url_or_id, timeout)
        )

    async def get_related_videos(
        self, url_or_id: str, timeout: int = 10
    ) -> Dict[str, Any]:
        """Get related videos for a YouTube video."""
        cache_key = self._generate_cache_key("related_videos", video=url_or_id)

        return await self._get_cached_or_fetch(
            cache_key, lambda: video.get_related_videos(url_or_id, timeout)
        )

    async def search_youtube(
        self, query: str, max_results: int = 10, timeout: int = 10
    ) -> Dict[str, Any]:
        """Search YouTube for videos."""
        cache_key = self._generate_cache_key(
            "search", query=query, max=max_results
        )

        # Search results have shorter TTL (30 minutes)
        return await self._get_cached_or_fetch(
            cache_key,
            lambda: search.search_youtube(query, max_results, timeout),
            ttl=1800,
        )
