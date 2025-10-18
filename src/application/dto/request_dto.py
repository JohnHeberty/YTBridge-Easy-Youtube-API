"""Data Transfer Objects (DTOs)."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ChannelRequestDTO:
    """DTO for channel request parameters."""
    
    channel_input: str
    include_videos: bool = True
    max_videos: int = 10
    timeout: int = 10

    def validate(self):
        """Validate request parameters."""
        if not self.channel_input or not self.channel_input.strip():
            raise ValueError("channel_input cannot be empty")
        if self.max_videos < 1 or self.max_videos > 100:
            raise ValueError("max_videos must be between 1 and 100")
        if self.timeout < 1 or self.timeout > 60:
            raise ValueError("timeout must be between 1 and 60 seconds")


@dataclass
class ChannelVideosRequestDTO:
    """DTO for channel videos request parameters."""
    
    channel_input: str
    max_results: int = 50
    timeout: int = 10

    def validate(self):
        """Validate request parameters."""
        if not self.channel_input or not self.channel_input.strip():
            raise ValueError("channel_input cannot be empty")
        if self.max_results < 1 or self.max_results > 200:
            raise ValueError("max_results must be between 1 and 200")
        if self.timeout < 1 or self.timeout > 60:
            raise ValueError("timeout must be between 1 and 60 seconds")


@dataclass
class PlaylistRequestDTO:
    """DTO for playlist request parameters."""
    
    url_or_id: str
    max_results: int = 50
    timeout: int = 10

    def validate(self):
        """Validate request parameters."""
        if not self.url_or_id or not self.url_or_id.strip():
            raise ValueError("url_or_id cannot be empty")
        if self.max_results < 1 or self.max_results > 200:
            raise ValueError("max_results must be between 1 and 200")
        if self.timeout < 1 or self.timeout > 60:
            raise ValueError("timeout must be between 1 and 60 seconds")


@dataclass
class VideoRequestDTO:
    """DTO for video request parameters."""
    
    url_or_id: str
    timeout: int = 10

    def validate(self):
        """Validate request parameters."""
        if not self.url_or_id or not self.url_or_id.strip():
            raise ValueError("url_or_id cannot be empty")
        if self.timeout < 1 or self.timeout > 60:
            raise ValueError("timeout must be between 1 and 60 seconds")


@dataclass
class SearchRequestDTO:
    """DTO for search request parameters."""
    
    query: str
    max_results: int = 10
    timeout: int = 10

    def validate(self):
        """Validate request parameters."""
        if not self.query or not self.query.strip():
            raise ValueError("query cannot be empty")
        if len(self.query) > 200:
            raise ValueError("query must be less than 200 characters")
        if self.max_results < 1 or self.max_results > 50:
            raise ValueError("max_results must be between 1 and 50")
        if self.timeout < 1 or self.timeout > 60:
            raise ValueError("timeout must be between 1 and 60 seconds")
