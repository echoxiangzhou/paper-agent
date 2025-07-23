"""
API router configuration for version 1.

Combines all API endpoints and configures the main API router.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users


api_router = APIRouter()

# Authentication routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"],
)

# User management routes
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)

# Health check for API
@api_router.get("/health")
async def api_health_check():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "service": "paper-agent-api",
        "version": "v1",
    }