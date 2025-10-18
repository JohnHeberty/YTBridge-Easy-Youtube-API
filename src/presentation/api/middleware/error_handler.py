"""Error handling middleware."""
import traceback
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.infrastructure.config import settings


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handler middleware."""

    async def dispatch(self, request: Request, call_next):
        """Handle errors globally."""
        try:
            response = await call_next(request)
            return response
        except ValueError as e:
            # Validation errors
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "error": "Validation Error",
                    "detail": str(e),
                },
            )
        except Exception as e:
            # Unexpected errors
            error_detail = str(e)
            
            # Include traceback in debug mode
            if settings.DEBUG:
                error_detail = f"{error_detail}\n\n{traceback.format_exc()}"
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": "Internal Server Error",
                    "detail": error_detail,
                },
            )
