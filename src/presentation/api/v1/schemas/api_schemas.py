"""Pydantic schemas for API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


# Channel Schemas
class ChannelInfoRequest(BaseModel):
    """Request schema for channel information."""
    
    channel_input: str = Field(..., description="Channel ID, username, handle or URL")
    include_videos: bool = Field(True, description="Whether to include recent videos")
    max_videos: int = Field(10, ge=1, le=100, description="Maximum number of videos")
    timeout: int = Field(10, ge=1, le=60, description="Request timeout in seconds")


class ChannelVideosRequest(BaseModel):
    """Request schema for channel videos."""
    
    channel_input: str = Field(..., description="Channel ID, username, handle or URL")
    max_results: int = Field(50, ge=1, le=200, description="Maximum number of videos")
    timeout: int = Field(10, ge=1, le=60, description="Request timeout in seconds")


# Playlist Schemas
class PlaylistInfoRequest(BaseModel):
    """Request schema for playlist information."""
    
    url_or_id: str = Field(..., description="Playlist URL or ID")
    max_results: int = Field(50, ge=1, le=200, description="Maximum number of videos")
    timeout: int = Field(10, ge=1, le=60, description="Request timeout in seconds")


# Video Schemas
class VideoInfoRequest(BaseModel):
    """Request schema for video information."""
    
    url_or_id: str = Field(..., description="Video URL or ID")
    timeout: int = Field(10, ge=1, le=60, description="Request timeout in seconds")


class RelatedVideosRequest(BaseModel):
    """Request schema for related videos."""
    
    url_or_id: str = Field(..., description="Video URL or ID")
    timeout: int = Field(10, ge=1, le=60, description="Request timeout in seconds")


# Search Schemas
class SearchRequest(BaseModel):
    """Request schema for YouTube search."""
    
    query: str = Field(..., description="Search query", max_length=200)
    max_results: int = Field(10, ge=1, le=50, description="Maximum number of results")
    timeout: int = Field(10, ge=1, le=60, description="Request timeout in seconds")


# Generic Response Schema
class APIResponse(BaseModel):
    """Generic API response schema."""
    
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if failed")
    message: Optional[str] = Field(None, description="Additional message")


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
