"""
FastAPI main application for Defeah Marketing Backend.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging

from app.core.config import settings
from app.core.database import create_tables
from app.core.redis import redis_manager
from app.api.v1 import auth, posts, campaigns, content, users, instagram
from app.utils.exceptions import setup_exception_handlers

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting up Defeah Marketing Backend...")
    
    # Create database tables
    create_tables()
    logger.info("Database tables created/verified")
    
    # Connect to Redis
    await redis_manager.connect()
    logger.info("Connected to Redis")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await redis_manager.disconnect()
    logger.info("Disconnected from Redis")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Autonomous Instagram Marketing System for Defeah Home Decor",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None
)

# Security middleware
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["api.defeah.com", "*.defeah.com"]
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include API routers
app.include_router(
    auth.router,
    prefix=settings.API_V1_STR,
    tags=["authentication"]
)

app.include_router(
    users.router,
    prefix=settings.API_V1_STR,
    tags=["users"]
)

app.include_router(
    posts.router,
    prefix=settings.API_V1_STR,
    tags=["posts"]
)

app.include_router(
    campaigns.router,
    prefix=settings.API_V1_STR,
    tags=["campaigns"]
)


app.include_router(
    content.router,
    prefix=settings.API_V1_STR,
    tags=["ai-content"]
)

app.include_router(
    instagram.router,
    prefix=settings.API_V1_STR,
    tags=["instagram"]
)

# Setup exception handlers
setup_exception_handlers(app)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {
            "database": "healthy",  # TODO: Add actual DB health check
            "redis": "healthy",     # TODO: Add actual Redis health check
            "instagram_api": "healthy",  # TODO: Add Instagram API health check
            "openai_api": "healthy"      # TODO: Add OpenAI API health check
        }
    }


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Root endpoint."""
    return {
        "message": "Defeah Marketing API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs" if settings.DEBUG else None
    }


@app.get("/info", status_code=status.HTTP_200_OK)
async def api_info():
    """API information endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "api_version": "v1",
        "features": {
            "instagram_integration": True,
            "ai_content_generation": True,
            "campaign_management": True,
            "real_time_updates": True
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=9000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )