"""Get related videos use case."""
from typing import List, Dict, Any
from src.domain.repositories import IYouTubeRepository
from src.application.dto import VideoRequestDTO


class GetRelatedVideosUseCase:
    """
    Use case for getting related videos.
    Follows Single Responsibility Principle (SRP).
    """

    def __init__(self, repository: IYouTubeRepository):
        """
        Initialize use case with repository.
        Dependency Injection following DIP.
        """
        self._repository = repository

    async def execute(self, request: VideoRequestDTO) -> List[Dict[str, Any]]:
        """
        Execute the use case.
        
        Args:
            request: Request DTO with video parameters
            
        Returns:
            List of related videos
            
        Raises:
            ValueError: If request validation fails
        """
        # Validate request
        request.validate()
        
        # Execute repository method
        result = await self._repository.get_related_videos(
            url_or_id=request.url_or_id,
            timeout=request.timeout
        )
        
        # Check for errors in result
        if isinstance(result, dict) and "error" in result:
            raise ValueError(f"Failed to get related videos: {result['error']}")
        
        return result
