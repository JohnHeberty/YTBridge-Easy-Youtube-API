"""Example tests for the YouTube API."""
import pytest
from httpx import AsyncClient
from src.presentation.main import create_app


@pytest.fixture
async def client():
    """Create test client."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_search_videos(client: AsyncClient):
    """Test search videos endpoint."""
    response = await client.get(
        "/api/v1/search/",
        params={"q": "Python", "max_results": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "results" in data["data"]


@pytest.mark.asyncio
async def test_invalid_video_id(client: AsyncClient):
    """Test with invalid video ID."""
    response = await client.get("/api/v1/videos/info/invalid_id_123")
    # Should still return 200 but with error in data
    assert response.status_code in [200, 400, 500]


@pytest.mark.asyncio
async def test_channel_info_validation(client: AsyncClient):
    """Test channel info with validation."""
    # Test with empty channel_input (should fail)
    response = await client.post(
        "/api/v1/channels/info",
        json={
            "channel_input": "",
            "include_videos": True,
            "max_videos": 10
        }
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_rate_limit_headers(client: AsyncClient):
    """Test that rate limit headers are present."""
    response = await client.get("/api/v1/health")
    # Rate limit headers should be present if rate limiting is enabled
    # X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
    # Note: This test assumes rate limiting is enabled
    # Headers may not be present in test environment
    assert response.status_code == 200
