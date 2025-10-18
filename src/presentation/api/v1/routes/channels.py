"""Channel routes."""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any
from src.presentation.api.v1.schemas import (
    APIResponse,
    ChannelInfoRequest,
    ChannelVideosRequest,
)
from src.application.use_cases import (
    GetChannelInfoUseCase,
    GetChannelVideosUseCase,
)
from src.application.dto import ChannelRequestDTO, ChannelVideosRequestDTO
from src.presentation.api.dependencies import get_channel_info_use_case, get_channel_videos_use_case


router = APIRouter(prefix="/channels", tags=["Channels"])


@router.post("/info", response_model=APIResponse, summary="Get channel information")
async def get_channel_info(
    request: ChannelInfoRequest,
    use_case: GetChannelInfoUseCase = Depends(get_channel_info_use_case),
) -> APIResponse:
    """
    Get detailed information about a YouTube channel.
    
    - **channel_input**: Channel ID, username, handle (@username), or URL
    - **include_videos**: Whether to include recent videos in response
    - **max_videos**: Maximum number of videos to include (1-100)
    - **timeout**: Request timeout in seconds (1-60)
    
    Returns channel metadata including title, description, subscriber count, etc.
    """
    try:
        dto = ChannelRequestDTO(
            channel_input=request.channel_input,
            include_videos=request.include_videos,
            max_videos=request.max_videos,
            timeout=request.timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/info/{channel_input}", response_model=APIResponse, summary="Get channel information (GET)")
async def get_channel_info_get(
    channel_input: str,
    include_videos: bool = Query(True, description="Include recent videos"),
    max_videos: int = Query(10, ge=1, le=100, description="Maximum videos"),
    timeout: int = Query(10, ge=1, le=60, description="Timeout in seconds"),
    use_case: GetChannelInfoUseCase = Depends(get_channel_info_use_case),
) -> APIResponse:
    """
    Get detailed information about a YouTube channel using GET method.
    
    Same as POST /info but using URL parameters.
    """
    try:
        dto = ChannelRequestDTO(
            channel_input=channel_input,
            include_videos=include_videos,
            max_videos=max_videos,
            timeout=timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/videos", response_model=APIResponse, summary="Get channel videos")
async def get_channel_videos(
    request: ChannelVideosRequest,
    use_case: GetChannelVideosUseCase = Depends(get_channel_videos_use_case),
) -> APIResponse:
    """
    Get videos from a YouTube channel.
    
    - **channel_input**: Channel ID, username, handle, or URL
    - **max_results**: Maximum number of videos to return (1-200)
    - **timeout**: Request timeout in seconds (1-60)
    
    Returns list of videos with basic information.
    """
    try:
        dto = ChannelVideosRequestDTO(
            channel_input=request.channel_input,
            max_results=request.max_results,
            timeout=request.timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/videos/{channel_input}", response_model=APIResponse, summary="Get channel videos (GET)")
async def get_channel_videos_get(
    channel_input: str,
    max_results: int = Query(50, ge=1, le=200, description="Maximum videos"),
    timeout: int = Query(10, ge=1, le=60, description="Timeout in seconds"),
    use_case: GetChannelVideosUseCase = Depends(get_channel_videos_use_case),
) -> APIResponse:
    """
    Get videos from a YouTube channel using GET method.
    
    Same as POST /videos but using URL parameters.
    """
    try:
        dto = ChannelVideosRequestDTO(
            channel_input=channel_input,
            max_results=max_results,
            timeout=timeout,
        )
        
        result = await use_case.execute(dto)
        
        return APIResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
