"""Get channel videos use case."""
from typing import Dict, Any
from src.domain.repositories import IYouTubeRepository
from src.application.dto import ChannelVideosRequestDTO


class GetChannelVideosUseCase:
    """
    Use case for getting channel videos.
    Follows Single Responsibility Principle (SRP).
    """

    def __init__(self, repository: IYouTubeRepository):
        """
        Initialize use case with repository.
        Dependency Injection following DIP.
        """
        self._repository = repository

    async def execute(self, request: ChannelVideosRequestDTO) -> Dict[str, Any]:
        """
        Execute the use case.
        
        Args:
            request: Request DTO with channel videos parameters
            
        Returns:
            Channel videos information dictionary
            
        Raises:
            ValueError: If request validation fails
        """
        # Validate request
        request.validate()
        
        # Execute repository method
        result = await self._repository.get_channel_videos(
            channel_input=request.channel_input,
            max_results=request.max_results,
            timeout=request.timeout
        )
        
        # Check for errors in result
        if "error" in result:
            raise ValueError(f"Failed to get channel videos: {result['error']}")
        
        return result
