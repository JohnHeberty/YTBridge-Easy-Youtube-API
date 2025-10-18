"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from src.presentation.api.v1.routes import channels, videos, playlists, search
from src.presentation.api.middleware import RateLimitMiddleware, ErrorHandlerMiddleware
from src.infrastructure.config import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
        ## YouTube Data API
        
        A powerful REST API for accessing YouTube data without requiring an API key.
        Built with Clean Architecture principles and SOLID design patterns.
        
        ### Features
        - ✅ **Channel Information**: Get detailed channel metadata and videos
        - ✅ **Video Information**: Retrieve video details including views, likes, and duration
        - ✅ **Playlist Data**: Access playlist information and video lists
        - ✅ **Search**: Search YouTube for videos
        - ✅ **Related Videos**: Find videos related to a specific video
        - ✅ **Caching**: Built-in caching support (Memory/Redis) to reduce load
        - ✅ **Rate Limiting**: Protect against abuse
        - ✅ **CORS Enabled**: Ready for web applications
        
        ### Authentication
        No authentication required! This API is free to use.
        
        ### Rate Limits
        - **{limit}** requests per minute per IP address
        
        ### Cache
        - Responses are cached for **{ttl}** seconds
        - Cache type: **{cache_type}**
        """.format(
            limit=settings.RATE_LIMIT_REQUESTS,
            ttl=settings.CACHE_TTL,
            cache_type=settings.CACHE_TYPE.upper()
        ),
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    # Add rate limiting middleware
    if settings.RATE_LIMIT_ENABLED:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_period=settings.RATE_LIMIT_REQUESTS,
            period=settings.RATE_LIMIT_PERIOD,
        )
    
    # Add error handler middleware
    app.add_middleware(ErrorHandlerMiddleware)
    
    # Include routers
    app.include_router(channels.router, prefix=settings.API_V1_PREFIX)
    app.include_router(videos.router, prefix=settings.API_V1_PREFIX)
    app.include_router(playlists.router, prefix=settings.API_V1_PREFIX)
    app.include_router(search.router, prefix=settings.API_V1_PREFIX)
    
    # Root endpoint
    @app.get("/", include_in_schema=False)
    async def root():
        """Redirect to API documentation."""
        return RedirectResponse(url=f"{settings.API_V1_PREFIX}/docs")
    
    # Health check endpoint
    @app.get(f"{settings.API_V1_PREFIX}/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint.
        
        Returns API status and configuration.
        """
        return {
            "status": "healthy",
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "cache_enabled": settings.CACHE_ENABLED,
            "cache_type": settings.CACHE_TYPE,
            "rate_limit_enabled": settings.RATE_LIMIT_ENABLED,
        }
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
    )
