"""
FastAPI main application for Defeah Marketing Backend.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from contextlib import asynccontextmanager
import logging
import asyncio
import time
import secrets

from app.core.database import create_tables, close_database_connections
from app.core.redis import test_redis_connection
from app.core.config import settings
from app.utils.exceptions import setup_exception_handlers
from app.utils.logging import setup_logging
from app.api import api_v1_router
from app.schemas import RootResponse, HealthResponse, ServiceStatus

# Setup logging
logger = setup_logging()
logger = logging.getLogger(__name__)


async def safe_health_check(check_func, service_name: str, *args, **kwargs) -> dict:
    """
    Safely execute a health check function with error handling.
    
    Args:
        check_func: The health check function to execute
        service_name: Name of the service being checked
        *args, **kwargs: Arguments to pass to the check function
        
    Returns:
        Dictionary with status and response time
    """
    try:
        start_time = time.time()
        is_healthy = await check_func(*args, **kwargs) if asyncio.iscoroutinefunction(check_func) else check_func(*args, **kwargs)
        response_time = round((time.time() - start_time) * 1000, 2)
        
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "response_time_ms": response_time
        }
    except Exception as e:
        logger.error("Health check failed for %s: %s", service_name, str(e))
        return {
            "status": "error",
            "response_time_ms": 0
        }


def generate_csp_nonce() -> str:
    """Generate a cryptographically secure nonce for CSP."""
    return secrets.token_urlsafe(16)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Generate nonce for this request
        nonce = generate_csp_nonce()
        
        # Store nonce in request state for potential use in templates
        request.state.csp_nonce = nonce
        
        # Add comprehensive security headers with nonce-based CSP
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; style-src 'self' 'nonce-{nonce}' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none';",
            "Permissions-Policy": "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()",
        }
        
        # Add HTTPS security headers in production
        if settings.ENVIRONMENT == "production":
            security_headers.update({
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
                "Expect-CT": "max-age=86400, enforce"
            })
        
        # Apply headers to response
        for header, value in security_headers.items():
            response.headers[header] = value
        
        return response


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
    description="""
    **Defeah Marketing Backend** - Autonomous Instagram Marketing System
    
    This API provides comprehensive Instagram marketing automation capabilities including:
    
    * **Authentication & User Management** - JWT-based authentication with role-based access
    * **AI Content Generation** - Automated caption and image creation using GPT-4 and DALL-E 3
    * **Post Management** - Create, schedule, and publish Instagram content
    * **Campaign Management** - Multi-post marketing campaign orchestration
    * **Analytics & Insights** - Performance tracking and optimization
    
    ## Authentication
    
    The API uses JWT Bearer token authentication. Include your access token in the Authorization header:
    
    ```
    Authorization: Bearer your_access_token_here
    ```
    
    ## Rate Limiting
    
    API endpoints are rate limited to prevent abuse:
    - Authentication endpoints: 5 attempts per minute
    - General endpoints: 1000 requests per hour per user
    - Global limit: 100,000 requests per hour
    
    Rate limit headers are included in all responses.
    
    ## Error Handling
    
    All errors follow a consistent format with appropriate HTTP status codes and detailed error messages.
    """,
    summary="Autonomous Instagram Marketing API for Defeah Home Decor Brand",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    contact={
        "name": "Defeah Marketing Team",
        "email": "dev@defeah.com",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://defeah.com/license",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.defeah.com",
            "description": "Production server"
        }
    ],
    tags_metadata=[
        {
            "name": "authentication",
            "description": "User authentication and authorization operations including registration, login, logout, and token management.",
        },
        {
            "name": "health",
            "description": "Application health monitoring and system status endpoints for load balancer health checks.",
        },
        {
            "name": "posts", 
            "description": "Instagram post management including creation, scheduling, publishing, and analytics.",
        },
        {
            "name": "campaigns",
            "description": "Multi-post marketing campaign management and orchestration.",
        },
        {
            "name": "content",
            "description": "AI-powered content generation using GPT-4 for captions and DALL-E 3 for images.",
        },
        {
            "name": "analytics",
            "description": "Performance analytics, insights, and optimization recommendations.",
        }
    ],
    lifespan=lifespan
)

# Setup exception handlers
setup_exception_handlers(app)

# Security middleware (applied in reverse order due to middleware stack)
# Add security headers to all responses
app.add_middleware(SecurityHeadersMiddleware)

# Trusted host middleware to prevent Host header attacks
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.TRUSTED_HOSTS
)

# CORS middleware with comprehensive security configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    expose_headers=settings.CORS_EXPOSE_HEADERS,
    max_age=settings.CORS_MAX_AGE,
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


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Comprehensive health check endpoint for load balancers and monitoring.
    
    Returns the current status of all critical system components including:
    - Database connectivity and response time
    - Redis cache connectivity 
    - External API dependencies
    - Application version and environment
    
    This endpoint requires no authentication and provides essential information
    for automated health monitoring and load balancer health checks.
    """
    from datetime import datetime
    from app.core.redis import test_redis_connection
    from app.core.database import check_database_connection
    
    start_time = time.time()
    
    # Test database connection with error handling
    db_result = await safe_health_check(check_database_connection, "database")
    
    # Test Redis connection with error handling
    redis_result = await safe_health_check(test_redis_connection, "redis")
    
    # Determine overall status based on critical services
    critical_services_healthy = all([
        db_result["status"] == "healthy",
        redis_result["status"] == "healthy"
    ])
    
    if critical_services_healthy:
        overall_status = "healthy"
    elif any(result["status"] == "error" for result in [db_result, redis_result]):
        overall_status = "unhealthy"
    else:
        overall_status = "degraded"
    
    total_response_time = round((time.time() - start_time) * 1000, 2)
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat() + "Z",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        services={
            "database": ServiceStatus(
                status=db_result["status"],
                response_time_ms=db_result["response_time_ms"]
            ),
            "redis": ServiceStatus(
                status=redis_result["status"],
                response_time_ms=redis_result["response_time_ms"]
            ),
            "instagram_api": ServiceStatus(
                status="not_configured",
                response_time_ms=0
            ),
            "openai_api": ServiceStatus(
                status="not_configured", 
                response_time_ms=0
            )
        },
        response_time_ms=total_response_time
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)