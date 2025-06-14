"""
API v1 router - Main router for version 1 of the API.
"""
from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.metrics import router as metrics_router

# Create main API router
api_router = APIRouter()

# Include health check routes
api_router.include_router(health_router, tags=["health"])

# Include metrics routes
api_router.include_router(metrics_router, tags=["metrics"])

# API v1 root endpoint
@api_router.get("/")
async def api_root():
    """API v1 root endpoint."""
    return {
        "message": "Defeah Marketing API v1",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "health_database": "/api/v1/health/database",
            "health_detailed": "/api/v1/health/detailed",
            "metrics": "/api/v1/metrics",
            "metrics_health": "/api/v1/metrics/health",
            "docs": "/docs"
        }
    }