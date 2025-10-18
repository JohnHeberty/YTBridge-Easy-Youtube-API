"""Playlist routes."""
from fastapi import APIRouter, HTTPException, Depends, Query
from src.presentation.api.v1.schemas import APIResponse, PlaylistInfoRequest
from src.application.use_cases import GetPlaylistInfoUseCase
from src.application.dto import PlaylistRequestDTO
from src.presentation.api.dependencies import get_playlist_info_use_case


router = APIRouter(prefix="/playlists", tags=["Playlists"])


@router.post("/info", response_model=APIResponse, summary="Get playlist information")
async def get_playlist_info(
    request: PlaylistInfoRequest,
    use_case: GetPlaylistInfoUseCase = Depends(get_playlist_info_use_case),
) -> APIResponse:
    """
    Get information about a YouTube playlist.
    
    - **url_or_id**: Playlist URL or playlist ID
    - **max_results**: Maximum number of videos to retrieve (1-200)
    - **timeout**: Request timeout in seconds (1-60)
    
    Returns playlist metadata and list of videos in the playlist.
    """
    try:
        dto = PlaylistRequestDTO(
            url_or_id=request.url_or_id,
            max_results=request.max_results,
            timeout=request.timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/info/{playlist_id}", response_model=APIResponse, summary="Get playlist information (GET)")
async def get_playlist_info_get(
    playlist_id: str,
    max_results: int = Query(50, ge=1, le=200, description="Maximum videos"),
    timeout: int = Query(10, ge=1, le=60, description="Timeout in seconds"),
    use_case: GetPlaylistInfoUseCase = Depends(get_playlist_info_use_case),
) -> APIResponse:
    """
    Get information about a YouTube playlist using GET method.
    
    Same as POST /info but using URL parameters.
    """
    try:
        dto = PlaylistRequestDTO(
            url_or_id=playlist_id,
            max_results=max_results,
            timeout=timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
