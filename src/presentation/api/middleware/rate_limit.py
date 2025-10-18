"""Rate limiting middleware."""
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from src.infrastructure.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting middleware.
    Tracks requests per IP address.
    """

    def __init__(self, app, requests_per_period: int = 100, period: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            app: FastAPI application
            requests_per_period: Maximum requests allowed per period
            period: Time period in seconds
        """
        super().__init__(app)
        self.requests_per_period = requests_per_period
        self.period = period
        self.request_counts = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host

        # Clean old timestamps
        current_time = time.time()
        self.request_counts[client_ip] = [
            timestamp
            for timestamp in self.request_counts[client_ip]
            if current_time - timestamp < self.period
        ]

        # Check rate limit
        if len(self.request_counts[client_ip]) >= self.requests_per_period:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {self.requests_per_period} requests per {self.period} seconds.",
            )

        # Add current request timestamp
        self.request_counts[client_ip].append(current_time)

        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_period)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_period - len(self.request_counts[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(self.request_counts[client_ip][0] + self.period)
        )

        return response
