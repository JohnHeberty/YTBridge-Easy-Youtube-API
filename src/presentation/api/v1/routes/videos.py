"""Video routes."""
from fastapi import APIRouter, HTTPException, Depends, Query
from src.presentation.api.v1.schemas import APIResponse, VideoInfoRequest, RelatedVideosRequest
from src.application.use_cases import GetVideoInfoUseCase, GetRelatedVideosUseCase
from src.application.dto import VideoRequestDTO
from src.presentation.api.dependencies import get_video_info_use_case, get_related_videos_use_case


router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post("/info", response_model=APIResponse, summary="Get video information")
async def get_video_info(
    request: VideoInfoRequest,
    use_case: GetVideoInfoUseCase = Depends(get_video_info_use_case),
) -> APIResponse:
    """
    Get detailed information about a YouTube video.
    
    - **url_or_id**: Video URL or video ID
    - **timeout**: Request timeout in seconds (1-60)
    
    Returns video metadata including title, description, views, duration, etc.
    """
    try:
        dto = VideoRequestDTO(
            url_or_id=request.url_or_id,
            timeout=request.timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/info/{video_id}", response_model=APIResponse, summary="Get video information (GET)")
async def get_video_info_get(
    video_id: str,
    timeout: int = Query(10, ge=1, le=60, description="Timeout in seconds"),
    use_case: GetVideoInfoUseCase = Depends(get_video_info_use_case),
) -> APIResponse:
    """
    Get detailed information about a YouTube video using GET method.
    
    Same as POST /info but using URL parameters.
    """
    try:
        dto = VideoRequestDTO(
            url_or_id=video_id,
            timeout=timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/related", response_model=APIResponse, summary="Get related videos")
async def get_related_videos(
    request: RelatedVideosRequest,
    use_case: GetRelatedVideosUseCase = Depends(get_related_videos_use_case),
) -> APIResponse:
    """
    Get videos related to a specific YouTube video.
    
    - **url_or_id**: Video URL or video ID
    - **timeout**: Request timeout in seconds (1-60)
    
    Returns list of related videos.
    """
    try:
        dto = VideoRequestDTO(
            url_or_id=request.url_or_id,
            timeout=request.timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/related/{video_id}", response_model=APIResponse, summary="Get related videos (GET)")
async def get_related_videos_get(
    video_id: str,
    timeout: int = Query(10, ge=1, le=60, description="Timeout in seconds"),
    use_case: GetRelatedVideosUseCase = Depends(get_related_videos_use_case),
) -> APIResponse:
    """
    Get videos related to a specific YouTube video using GET method.
    
    Same as POST /related but using URL parameters.
    """
    try:
        dto = VideoRequestDTO(
            url_or_id=video_id,
            timeout=timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
