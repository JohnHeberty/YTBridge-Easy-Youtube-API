"""Channel entity - Domain layer."""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Channel:
    """Channel entity representing a YouTube channel."""
    
    channel_id: str
    title: str
    channel_url: Optional[str] = None
    description: Optional[str] = None
    description_snippet: Optional[str] = None
    handle: Optional[str] = None
    handle_name: Optional[str] = None
    vanity_url: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    subscriber_count_text: Optional[str] = None
    subscriber_count_approximate: Optional[int] = None
    video_count: Optional[int] = None
    view_count: Optional[int] = None
    joined_date: Optional[str] = None
    location: Optional[str] = None
    avatar_thumbnails: Optional[List[Dict[str, Any]]] = None
    banner_thumbnails: Optional[List[Dict[str, Any]]] = None
    external_links: Optional[List[Dict[str, str]]] = None
    videos: Optional[List[Dict[str, Any]]] = None
    videos_count: Optional[int] = None

    def __post_init__(self):
        """Validate channel entity."""
        if not self.channel_id:
            raise ValueError("channel_id is required")
        if not self.title:
            raise ValueError("title is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            "channel_id": self.channel_id,
            "title": self.title,
            "channel_url": self.channel_url,
            "description": self.description,
            "description_snippet": self.description_snippet,
            "handle": self.handle,
            "handle_name": self.handle_name,
            "vanity_url": self.vanity_url,
            "logo_url": self.logo_url,
            "banner_url": self.banner_url,
            "subscriber_count_text": self.subscriber_count_text,
            "subscriber_count_approximate": self.subscriber_count_approximate,
            "video_count": self.video_count,
            "view_count": self.view_count,
            "joined_date": self.joined_date,
            "location": self.location,
            "avatar_thumbnails": self.avatar_thumbnails,
            "banner_thumbnails": self.banner_thumbnails,
            "external_links": self.external_links,
            "videos": self.videos,
            "videos_count": self.videos_count,
        }
