"""Get playlist information use case."""
from typing import Dict, Any
from src.domain.repositories import IYouTubeRepository
from src.application.dto import PlaylistRequestDTO


class GetPlaylistInfoUseCase:
    """
    Use case for getting playlist information.
    Follows Single Responsibility Principle (SRP).
    """

    def __init__(self, repository: IYouTubeRepository):
        """
        Initialize use case with repository.
        Dependency Injection following DIP.
        """
        self._repository = repository

    async def execute(self, request: PlaylistRequestDTO) -> Dict[str, Any]:
        """
        Execute the use case.
        
        Args:
            request: Request DTO with playlist parameters
            
        Returns:
            Playlist information dictionary
            
        Raises:
            ValueError: If request validation fails
        """
        # Validate request
        request.validate()
        
        # Execute repository method
        result = await self._repository.get_playlist_info(
            url_or_id=request.url_or_id,
            max_results=request.max_results,
            timeout=request.timeout
        )
        
        # Check for errors in result
        if "error" in result:
            raise ValueError(f"Failed to get playlist info: {result['error']}")
        
        return result
