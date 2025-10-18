"""Dependency injection for FastAPI."""
from functools import lru_cache
from src.application.use_cases import (
    GetChannelInfoUseCase,
    GetChannelVideosUseCase,
    GetVideoInfoUseCase,
    GetRelatedVideosUseCase,
    GetPlaylistInfoUseCase,
    SearchYouTubeUseCase,
)
from src.infrastructure.repositories import YTBPyRepository
from src.infrastructure.cache import create_cache, ICache
from src.infrastructure.config import settings


# Cache singleton
_cache_instance: ICache = None


def get_cache() -> ICache:
    """Get or create cache instance (singleton)."""
    global _cache_instance
    
    if _cache_instance is None and settings.CACHE_ENABLED:
        _cache_instance = create_cache(
            cache_type=settings.CACHE_TYPE,
            max_size=settings.CACHE_MAX_SIZE,
            default_ttl=settings.CACHE_TTL,
            redis_host=settings.REDIS_HOST,
            redis_port=settings.REDIS_PORT,
            redis_db=settings.REDIS_DB,
            redis_password=settings.REDIS_PASSWORD,
        )
    
    return _cache_instance


@lru_cache()
def get_repository() -> YTBPyRepository:
    """Get repository instance (singleton)."""
    cache = get_cache() if settings.CACHE_ENABLED else None
    return YTBPyRepository(cache=cache)


# Use case dependencies
def get_channel_info_use_case() -> GetChannelInfoUseCase:
    """Get channel info use case with injected dependencies."""
    return GetChannelInfoUseCase(repository=get_repository())


def get_channel_videos_use_case() -> GetChannelVideosUseCase:
    """Get channel videos use case with injected dependencies."""
    return GetChannelVideosUseCase(repository=get_repository())


def get_video_info_use_case() -> GetVideoInfoUseCase:
    """Get video info use case with injected dependencies."""
    return GetVideoInfoUseCase(repository=get_repository())


def get_related_videos_use_case() -> GetRelatedVideosUseCase:
    """Get related videos use case with injected dependencies."""
    return GetRelatedVideosUseCase(repository=get_repository())


def get_playlist_info_use_case() -> GetPlaylistInfoUseCase:
    """Get playlist info use case with injected dependencies."""
    return GetPlaylistInfoUseCase(repository=get_repository())


def get_search_youtube_use_case() -> SearchYouTubeUseCase:
    """Get search YouTube use case with injected dependencies."""
    return SearchYouTubeUseCase(repository=get_repository())
