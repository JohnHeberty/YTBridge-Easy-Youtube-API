"""Get video information use case."""
from typing import Dict, Any
from src.domain.repositories import IYouTubeRepository
from src.application.dto import VideoRequestDTO


class GetVideoInfoUseCase:
    """
    Use case for getting video information.
    Follows Single Responsibility Principle (SRP).
    """

    def __init__(self, repository: IYouTubeRepository):
        """
        Initialize use case with repository.
        Dependency Injection following DIP.
        """
        self._repository = repository

    async def execute(self, request: VideoRequestDTO) -> Dict[str, Any]:
        """
        Execute the use case.
        
        Args:
            request: Request DTO with video parameters
            
        Returns:
            Video information dictionary
            
        Raises:
            ValueError: If request validation fails
        """
        # Validate request
        request.validate()
        
        # Execute repository method
        result = await self._repository.get_video_info(
            url_or_id=request.url_or_id,
            timeout=request.timeout
        )
        
        # Check for errors in result
        if "error" in result:
            raise ValueError(f"Failed to get video info: {result['error']}")
        
        return result
