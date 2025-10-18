"""Get channel information use case."""
from typing import Dict, Any
from src.domain.repositories import IYouTubeRepository
from src.application.dto import ChannelRequestDTO


class GetChannelInfoUseCase:
    """
    Use case for getting channel information.
    Follows Single Responsibility Principle (SRP).
    """

    def __init__(self, repository: IYouTubeRepository):
        """
        Initialize use case with repository.
        Dependency Injection following DIP.
        """
        self._repository = repository

    async def execute(self, request: ChannelRequestDTO) -> Dict[str, Any]:
        """
        Execute the use case.
        
        Args:
            request: Request DTO with channel parameters
            
        Returns:
            Channel information dictionary
            
        Raises:
            ValueError: If request validation fails
        """
        # Validate request
        request.validate()
        
        # Execute repository method
        result = await self._repository.get_channel_info(
            channel_input=request.channel_input,
            include_videos=request.include_videos,
            max_videos=request.max_videos,
            timeout=request.timeout
        )
        
        # Check for errors in result
        if "error" in result:
            raise ValueError(f"Failed to get channel info: {result['error']}")
        
        return result
