"""YouTube repository interface - Domain layer."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class IYouTubeRepository(ABC):
    """
    Interface for YouTube data repository.
    Following Interface Segregation Principle (ISP) and 
    Dependency Inversion Principle (DIP) from SOLID.
    """

    @abstractmethod
    async def get_channel_info(
        self, 
        channel_input: str, 
        include_videos: bool = True, 
        max_videos: int = 10,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Get detailed information about a YouTube channel.
        
        Args:
            channel_input: Channel ID, username, handle or URL
            include_videos: Whether to include recent videos
            max_videos: Maximum number of videos to include
            timeout: Request timeout in seconds
            
        Returns:
            Channel information dictionary
        """
        pass

    @abstractmethod
    async def get_channel_videos(
        self, 
        channel_input: str, 
        max_results: int = 50,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Get videos from a YouTube channel.
        
        Args:
            channel_input: Channel ID, username, handle or URL
            max_results: Maximum number of videos to return
            timeout: Request timeout in seconds
            
        Returns:
            Channel videos information
        """
        pass

    @abstractmethod
    async def get_playlist_info(
        self, 
        url_or_id: str, 
        max_results: int = 50,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Get information about a YouTube playlist.
        
        Args:
            url_or_id: Playlist URL or ID
            max_results: Maximum number of videos to retrieve
            timeout: Request timeout in seconds
            
        Returns:
            Playlist information dictionary
        """
        pass

    @abstractmethod
    async def get_video_info(
        self, 
        url_or_id: str,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Get detailed information about a YouTube video.
        
        Args:
            url_or_id: Video URL or ID
            timeout: Request timeout in seconds
            
        Returns:
            Video information dictionary
        """
        pass

    @abstractmethod
    async def get_related_videos(
        self, 
        url_or_id: str,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Get related videos for a YouTube video.
        
        Args:
            url_or_id: Video URL or ID
            timeout: Request timeout in seconds
            
        Returns:
            List of related videos
        """
        pass

    @abstractmethod
    async def search_youtube(
        self, 
        query: str, 
        max_results: int = 10,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Search YouTube for videos.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            timeout: Request timeout in seconds
            
        Returns:
            Search results dictionary
        """
        pass
