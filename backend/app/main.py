"""
FastAPI main application for Defeah Marketing Backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.database import create_tables, close_database_connections
from app.core.redis import test_redis_connection
from app.core.config import settings
from app.utils.exceptions import setup_exception_handlers
from app.utils.logging import setup_logging
from app.api import api_v1_router
from app.schemas import RootResponse, HealthResponse

# Setup logging
logger = setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting up Defeah Marketing Backend...")
    
    # Create database tables
    await create_tables()
    logger.info("Database tables created/verified")
    
    # Test Redis connection
    if test_redis_connection():
        logger.info("Redis connection successful")
    else:
        logger.warning("Redis connection failed")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await close_database_connections()
    logger.info("Database connections closed")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Autonomous Instagram Marketing System for Defeah Home Decor",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Setup exception handlers
setup_exception_handlers(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_v1_router, prefix=settings.API_V1_STR, tags=["api-v1"])


@app.get("/", response_model=RootResponse)
async def root():
    """Root endpoint."""
    return RootResponse(
        message=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        docs_url="/docs" if settings.DEBUG else None
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    from app.core.redis import test_redis_connection
    
    return HealthResponse(
        status="healthy",
        services={
            "database": "connected",
            "redis": "connected" if test_redis_connection() else "disconnected"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)