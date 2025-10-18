"""Video entity - Domain layer."""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Video:
    """Video entity representing a YouTube video."""
    
    video_id: str
    title: Optional[str] = None
    thumbnails: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    duration_seconds: Optional[int] = None
    views_count: Optional[int] = None
    view_count_text: Optional[str] = None
    likes_count: Optional[int] = None
    publish_date: Optional[int] = None
    publish_date_text: Optional[str] = None
    upload_date: Optional[int] = None
    upload_date_text: Optional[str] = None
    published_time: Optional[str] = None
    approximate_upload_date: Optional[str] = None
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None
    channel_url: Optional[str] = None
    author_name: Optional[str] = None
    is_live: Optional[bool] = False
    is_private: Optional[bool] = False
    category: Optional[str] = None
    keywords: Optional[List[str]] = None
    badges: Optional[List[str]] = None
    chapters: Optional[List[Dict[str, Any]]] = None
    formats: Optional[List[Dict[str, Any]]] = None

    def __post_init__(self):
        """Validate video entity."""
        if not self.video_id:
            raise ValueError("video_id is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            "video_id": self.video_id,
            "title": self.title,
            "thumbnails": self.thumbnails,
            "url": self.url,
            "description": self.description,
            "duration": self.duration,
            "duration_seconds": self.duration_seconds,
            "views_count": self.views_count,
            "view_count_text": self.view_count_text,
            "likes_count": self.likes_count,
            "publish_date": self.publish_date,
            "publish_date_text": self.publish_date_text,
            "upload_date": self.upload_date,
            "upload_date_text": self.upload_date_text,
            "published_time": self.published_time,
            "approximate_upload_date": self.approximate_upload_date,
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "channel_url": self.channel_url,
            "author_name": self.author_name,
            "is_live": self.is_live,
            "is_private": self.is_private,
            "category": self.category,
            "keywords": self.keywords,
            "badges": self.badges,
            "chapters": self.chapters,
            "formats": self.formats,
        }
