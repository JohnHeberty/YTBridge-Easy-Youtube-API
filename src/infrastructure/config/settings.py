"""Configuration settings for the API."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings using Pydantic for environment variable management.
    """
    
    # API Settings
    APP_NAME: str = "YTBridge"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # Cache Settings
    CACHE_ENABLED: bool = True
    CACHE_TYPE: str = "memory"  # "memory" or "redis"
    CACHE_TTL: int = 3600  # 1 hour in seconds
    CACHE_MAX_SIZE: int = 1000  # Maximum items in memory cache
    
    # Redis Settings (if using redis cache)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100  # requests per minute
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # YouTube API Settings
    DEFAULT_TIMEOUT: int = 10  # seconds
    MAX_VIDEOS_PER_REQUEST: int = 100
    MAX_SEARCH_RESULTS: int = 50
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
