"""
API v1 router - Main router for version 1 of the API.
"""
from fastapi import APIRouter

# Create main API router
api_router = APIRouter()

# Health check endpoint for API v1
@api_router.get("/health")
async def api_health():
    """API v1 health check endpoint."""
    return {"status": "healthy", "version": "v1"}

# Placeholder for future endpoints
@api_router.get("/")
async def api_root():
    """API v1 root endpoint."""
    return {
        "message": "Defeah Marketing API v1",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "docs": "/docs"
        }
    }