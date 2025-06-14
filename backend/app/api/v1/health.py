"""
Health check endpoints for monitoring database and service status.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_async_db, check_database_connection
from app.schemas.common import HealthCheckResponse
from app.core.metrics import (
    track_health_check_metrics,
    update_connection_pool_metrics
)
from app.core.circuit_breaker import health_check_circuit_breaker, CircuitBreakerError

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
@track_health_check_metrics("basic")
async def health_check():
    """
    Basic health check endpoint.
    Returns application status and version info.
    """
    return HealthCheckResponse(
        status="healthy",
        message="Defeah Marketing Backend is running",
        version="1.0.0"
    )


@router.get("/health/database", response_model=HealthCheckResponse)
@track_health_check_metrics("database")
async def database_health_check():
    """
    Database health check endpoint with circuit breaker protection.
    Verifies database connection and basic query functionality.
    """
    try:
        # Use circuit breaker for database health check
        is_healthy = await health_check_circuit_breaker.call(check_database_connection)

        if is_healthy:
            return HealthCheckResponse(
                status="healthy",
                message="Database connection is healthy",
                version="1.0.0"
            )

        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )
    except CircuitBreakerError as e:
        logger.warning("Database health check circuit breaker open: %s", e)
        raise HTTPException(
            status_code=503,
            detail="Database health check temporarily unavailable (circuit breaker open)"
        ) from e
    except Exception as e:
        logger.error("Database health check failed: %s", e)
        raise HTTPException(
            status_code=503,
            detail=f"Database health check failed: {str(e)}"
        ) from e


@router.get("/health/detailed", response_model=dict)
@track_health_check_metrics("detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_async_db)):
    """
    Detailed health check endpoint with comprehensive metrics.
    Provides system status including database metrics and circuit breaker stats.
    """
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))

        # Update connection pool metrics
        update_connection_pool_metrics()

        # Get database connection pool status
        from app.core.database import get_async_engine  # pylint: disable=import-outside-toplevel
        engine = get_async_engine()
        pool = engine.pool

        # Get available pool metrics (async pools have different attributes)
        pool_status = {
            "size": getattr(pool, '_pool_size', 'unknown'),
            "max_overflow": getattr(pool, '_max_overflow', 'unknown'),
            "pool_class": pool.__class__.__name__,
            "status": "operational"
        }
        
        # Try to get additional metrics if available
        try:
            if hasattr(pool, 'size'):
                pool_status["current_size"] = pool.size()
            if hasattr(pool, 'checked_in'):
                pool_status["checked_in"] = pool.checkedin()
            if hasattr(pool, 'checked_out'):
                pool_status["checked_out"] = pool.checkedout()
        except Exception:  # pylint: disable=broad-except
            # Some methods might not be available on async pools
            pass

        # Get circuit breaker statistics
        circuit_breaker_stats = health_check_circuit_breaker.get_stats()
        
        return {
            "status": "healthy",
            "message": "All systems operational",
            "version": "1.0.0",
            "database": {
                "status": "healthy",
                "connection_pool": pool_status
            },
            "services": {
                "api": "healthy",
                "database": "healthy"
            },
            "circuit_breakers": {
                "health_check": circuit_breaker_stats
            },
            "metrics": {
                "prometheus_metrics": "Available via /api/v1/metrics endpoint",
                "health_metrics": "Available via /api/v1/metrics/health endpoint"
            }
        }

    except Exception as e:
        logger.error("Detailed health check failed: %s", e)
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        ) from e