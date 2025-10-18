"""Search YouTube use case."""
from typing import Dict, Any
from src.domain.repositories import IYouTubeRepository
from src.application.dto import SearchRequestDTO


class SearchYouTubeUseCase:
    """
    Use case for searching YouTube.
    Follows Single Responsibility Principle (SRP).
    """

    def __init__(self, repository: IYouTubeRepository):
        """
        Initialize use case with repository.
        Dependency Injection following DIP.
        """
        self._repository = repository

    async def execute(self, request: SearchRequestDTO) -> Dict[str, Any]:
        """
        Execute the use case.
        
        Args:
            request: Request DTO with search parameters
            
        Returns:
            Search results dictionary
            
        Raises:
            ValueError: If request validation fails
        """
        # Validate request
        request.validate()
        
        # Execute repository method
        result = await self._repository.search_youtube(
            query=request.query,
            max_results=request.max_results,
            timeout=request.timeout
        )
        
        # Check for errors in result
        if "error" in result:
            raise ValueError(f"Search failed: {result['error']}")
        
        return result
