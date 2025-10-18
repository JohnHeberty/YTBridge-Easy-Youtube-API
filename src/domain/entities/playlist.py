"""Playlist entity - Domain layer."""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Playlist:
    """Playlist entity representing a YouTube playlist."""
    
    playlist_id: str
    title: Optional[str] = None
    playlist_url: Optional[str] = None
    description: Optional[str] = None
    video_count: Optional[int] = None
    view_count: Optional[int] = None
    last_updated: Optional[str] = None
    privacy: Optional[str] = None
    thumbnails: Optional[List[Dict[str, Any]]] = None
    owner: Optional[str] = None
    owner_id: Optional[str] = None
    owner_url: Optional[str] = None
    videos: Optional[List[Dict[str, Any]]] = None
    videos_count: Optional[int] = None
    pages_fetched: Optional[int] = None
    total_videos: Optional[int] = None

    def __post_init__(self):
        """Validate playlist entity."""
        if not self.playlist_id:
            raise ValueError("playlist_id is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            "playlist_id": self.playlist_id,
            "title": self.title,
            "playlist_url": self.playlist_url,
            "description": self.description,
            "video_count": self.video_count,
            "view_count": self.view_count,
            "last_updated": self.last_updated,
            "privacy": self.privacy,
            "thumbnails": self.thumbnails,
            "owner": self.owner,
            "owner_id": self.owner_id,
            "owner_url": self.owner_url,
            "videos": self.videos,
            "videos_count": self.videos_count,
            "pages_fetched": self.pages_fetched,
            "total_videos": self.total_videos,
        }
