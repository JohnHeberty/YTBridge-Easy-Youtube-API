"""Search routes."""
from fastapi import APIRouter, HTTPException, Depends, Query
from src.presentation.api.v1.schemas import APIResponse, SearchRequest
from src.application.use_cases import SearchYouTubeUseCase
from src.application.dto import SearchRequestDTO
from src.presentation.api.dependencies import get_search_youtube_use_case


router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/", response_model=APIResponse, summary="Search YouTube")
async def search_youtube(
    request: SearchRequest,
    use_case: SearchYouTubeUseCase = Depends(get_search_youtube_use_case),
) -> APIResponse:
    """
    Search YouTube for videos.
    
    - **query**: Search query string (max 200 characters)
    - **max_results**: Maximum number of results to return (1-50)
    - **timeout**: Request timeout in seconds (1-60)
    
    Returns list of videos matching the search query.
    """
    try:
        dto = SearchRequestDTO(
            query=request.query,
            max_results=request.max_results,
            timeout=request.timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=APIResponse, summary="Search YouTube (GET)")
async def search_youtube_get(
    q: str = Query(..., description="Search query", max_length=200),
    max_results: int = Query(10, ge=1, le=50, description="Maximum results"),
    timeout: int = Query(10, ge=1, le=60, description="Timeout in seconds"),
    use_case: SearchYouTubeUseCase = Depends(get_search_youtube_use_case),
) -> APIResponse:
    """
    Search YouTube for videos using GET method.
    
    Same as POST / but using URL parameters.
    """
    try:
        dto = SearchRequestDTO(
            query=q,
            max_results=max_results,
            timeout=timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
