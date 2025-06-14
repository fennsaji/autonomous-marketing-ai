"""
Prometheus metrics for database and application monitoring.
"""
import time
from functools import wraps
from typing import Callable, Any
import logging
from prometheus_client import Counter, Histogram, Gauge, Info

logger = logging.getLogger(__name__)

# Database Connection Metrics
db_connections_total = Counter(
    'db_connections_total',
    'Total number of database connections created',
    ['engine_type', 'status']
)

db_connection_pool_size = Gauge(
    'db_connection_pool_size',
    'Current size of database connection pool',
    ['engine_type']
)

db_connection_pool_checked_out = Gauge(
    'db_connection_pool_checked_out',
    'Number of connections currently checked out from pool',
    ['engine_type']
)

db_connection_pool_checked_in = Gauge(
    'db_connection_pool_checked_in',
    'Number of connections currently checked in to pool',
    ['engine_type']
)

# Database Query Metrics
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Time spent executing database queries',
    ['operation', 'status'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

db_queries_total = Counter(
    'db_queries_total',
    'Total number of database queries executed',
    ['operation', 'status']
)

# Health Check Metrics
health_check_duration_seconds = Histogram(
    'health_check_duration_seconds',
    'Time spent executing health checks',
    ['check_type', 'status'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

health_checks_total = Counter(
    'health_checks_total',
    'Total number of health checks performed',
    ['check_type', 'status']
)

# Application Metrics
app_requests_total = Counter(
    'app_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

app_request_duration_seconds = Histogram(
    'app_request_duration_seconds',
    'Time spent processing HTTP requests',
    ['method', 'endpoint', 'status_code'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# Database Session Metrics
db_sessions_active = Gauge(
    'db_sessions_active',
    'Number of active database sessions',
    ['session_type']
)

db_session_errors_total = Counter(
    'db_session_errors_total',
    'Total number of database session errors',
    ['error_type', 'session_type']
)

# Retry Metrics
db_retry_attempts_total = Counter(
    'db_retry_attempts_total',
    'Total number of database retry attempts',
    ['operation', 'attempt_number']
)

# Application Info
app_info = Info(
    'app_info',
    'Application information'
)

# Set application info
app_info.info({
    'version': '1.0.0',
    'environment': 'development',
    'component': 'defeah_marketing_backend'
})


def track_db_query_metrics(operation: str):
    """
    Decorator to track database query metrics.

    Args:
        operation: Name of the database operation (e.g., 'select', 'insert', 'health_check')
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            status = 'success'

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = 'error'
                logger.error("Database operation %s failed: %s", operation, e)
                raise
            finally:
                duration = time.time() - start_time

                # Update metrics
                db_query_duration_seconds.labels(
                    operation=operation,
                    status=status
                ).observe(duration)

                db_queries_total.labels(
                    operation=operation,
                    status=status
                ).inc()

        return wrapper
    return decorator


def track_health_check_metrics(check_type: str):
    """
    Decorator to track health check metrics.

    Args:
        check_type: Type of health check (e.g., 'basic', 'database', 'detailed')
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            status = 'success'

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = 'error'
                logger.error("Health check %s failed: %s", check_type, e)
                raise
            finally:
                duration = time.time() - start_time

                # Update metrics
                health_check_duration_seconds.labels(
                    check_type=check_type,
                    status=status
                ).observe(duration)

                health_checks_total.labels(
                    check_type=check_type,
                    status=status
                ).inc()

        return wrapper
    return decorator


def update_connection_pool_metrics():
    """Update connection pool metrics from current engine state."""
    try:
        from app.core.database import get_async_engine, get_sync_engine

        # Update async engine metrics
        try:
            async_engine = get_async_engine()
            if async_engine and hasattr(async_engine, 'pool'):
                pool = async_engine.pool

                if hasattr(pool, 'size'):
                    db_connection_pool_size.labels(engine_type='async').set(pool.size())

                if hasattr(pool, 'checkedout'):
                    db_connection_pool_checked_out.labels(engine_type='async').set(pool.checkedout())

                if hasattr(pool, 'checkedin'):
                    db_connection_pool_checked_in.labels(engine_type='async').set(pool.checkedin())

        except Exception as e:
            logger.warning("Failed to update async engine metrics: %s", e)

        # Update sync engine metrics
        try:
            sync_engine = get_sync_engine()
            if sync_engine and hasattr(sync_engine, 'pool'):
                pool = sync_engine.pool

                if hasattr(pool, 'size'):
                    db_connection_pool_size.labels(engine_type='sync').set(pool.size())

                if hasattr(pool, 'checkedout'):
                    db_connection_pool_checked_out.labels(engine_type='sync').set(pool.checkedout())

                if hasattr(pool, 'checkedin'):
                    db_connection_pool_checked_in.labels(engine_type='sync').set(pool.checkedin())

        except Exception as e:
            logger.warning("Failed to update sync engine metrics: %s", e)

    except Exception as e:
        logger.error("Failed to update connection pool metrics: %s", e)


def track_retry_attempt(operation: str, attempt_number: int):
    """Track database retry attempts."""
    db_retry_attempts_total.labels(
        operation=operation,
        attempt_number=str(attempt_number)
    ).inc()


def increment_db_connection_counter(engine_type: str, status: str):
    """Increment database connection counter."""
    db_connections_total.labels(
        engine_type=engine_type,
        status=status
    ).inc()


def track_session_error(error_type: str, session_type: str):
    """Track database session errors."""
    db_session_errors_total.labels(
        error_type=error_type,
        session_type=session_type
    ).inc()