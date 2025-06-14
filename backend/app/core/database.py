"""
Database configuration and connection management with async support.
Enhanced with timeout configuration, retry logic, and observability.
"""
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import logging
import asyncio
import time
from functools import wraps

from app.core.config import settings
from app.core.metrics import (
    track_db_query_metrics, 
    increment_db_connection_counter, 
    track_session_error,
    track_retry_attempt
)

logger = logging.getLogger(__name__)

# Global engine variables
async_engine = None
sync_engine = None


def retry_with_exponential_backoff(max_attempts: int = None, base_delay: float = None):
    """
    Decorator for implementing exponential backoff retry logic.
    
    Args:
        max_attempts: Maximum number of retry attempts (from settings if None)
        base_delay: Base delay in seconds (from settings if None)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempts = max_attempts or settings.DB_RETRY_ATTEMPTS
            delay = base_delay or settings.DB_RETRY_DELAY
            
            for attempt in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    # Track retry attempt
                    track_retry_attempt(func.__name__, attempt + 1)
                    
                    if attempt == attempts - 1:  # Last attempt
                        logger.error(f"Final attempt failed for {func.__name__}: {e}")
                        raise
                    
                    # Calculate delay with exponential backoff
                    current_delay = min(
                        delay * (settings.DB_RETRY_BACKOFF ** attempt),
                        settings.DB_RETRY_MAX_DELAY
                    )
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {current_delay:.2f} seconds..."
                    )
                    await asyncio.sleep(current_delay)
                    
        return wrapper
    return decorator


def get_async_engine():
    """Get or create async database engine with enhanced configuration."""
    global async_engine
    if async_engine is None:
        # Prepare connection arguments with timeouts
        connect_args = {
            "server_settings": {
                "jit": "off",  # Disable JIT for faster connection
            }
        }
        
        # Add timeout configurations for asyncpg
        if "asyncpg" in settings.DATABASE_URL_ASYNC:
            connect_args.update({
                "command_timeout": settings.DB_COMMAND_TIMEOUT,
                "server_settings": {
                    **connect_args.get("server_settings", {}),
                    "statement_timeout": f"{settings.DB_COMMAND_TIMEOUT * 1000}ms",
                }
            })
        
        async_engine = create_async_engine(
            settings.DATABASE_URL_ASYNC,
            echo=settings.DEBUG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_pre_ping=settings.DB_POOL_PRE_PING,
            pool_recycle=settings.DB_POOL_RECYCLE,
            poolclass=StaticPool if "test" in settings.DATABASE_URL_ASYNC else None,
            connect_args=connect_args,
            # Connection timeout
            pool_timeout=settings.DB_CONNECT_TIMEOUT,
        )
        logger.info(f"Created async database engine with pool_size={settings.DB_POOL_SIZE}, max_overflow={settings.DB_MAX_OVERFLOW}")
        increment_db_connection_counter("async", "created")
    return async_engine


def get_sync_engine():
    """Get or create sync database engine with enhanced configuration."""
    global sync_engine
    if sync_engine is None:
        # Prepare connection arguments with timeouts
        connect_args = {}
        
        # Add timeout configurations for psycopg2
        if "postgresql" in settings.DATABASE_URL and "asyncpg" not in settings.DATABASE_URL:
            connect_args.update({
                "connect_timeout": settings.DB_CONNECT_TIMEOUT,
                "options": f"-c statement_timeout={settings.DB_COMMAND_TIMEOUT * 1000}ms"
            })
        
        sync_engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_pre_ping=settings.DB_POOL_PRE_PING,
            pool_recycle=settings.DB_POOL_RECYCLE,
            connect_args=connect_args,
            pool_timeout=settings.DB_CONNECT_TIMEOUT,
        )
        logger.info(f"Created sync database engine with pool_size={settings.DB_POOL_SIZE}, max_overflow={settings.DB_MAX_OVERFLOW}")
        increment_db_connection_counter("sync", "created")
    return sync_engine

# Session factory functions
def get_async_session_factory():
    """Get async session factory."""
    return async_sessionmaker(
        bind=get_async_engine(),
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


def get_sync_session_factory():
    """Get sync session factory."""
    return sessionmaker(autocommit=False, autoflush=False, bind=get_sync_engine())

# Create base class for models
Base = declarative_base()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session with retry logic."""
    async_session_factory = get_async_session_factory()
    
    @retry_with_exponential_backoff(max_attempts=2, base_delay=0.5)  # Quick retry for sessions
    async def get_session():
        return async_session_factory()
    
    try:
        session = await get_session()
        async with session:
            try:
                yield session
            except Exception as e:
                logger.error(f"Database session error: {e}")
                track_session_error(str(type(e).__name__), "async")
                await session.rollback()
                raise
            finally:
                await session.close()
    except Exception as e:
        logger.error(f"Failed to create database session after retries: {e}")
        raise


def get_db():
    """Dependency to get sync database session (for migrations)."""
    sync_session_factory = get_sync_session_factory()
    db = sync_session_factory()
    try:
        yield db
    finally:
        db.close()


@retry_with_exponential_backoff()
@track_db_query_metrics("create_tables")
async def create_tables():
    """Create all database tables asynchronously with retry logic."""
    # Import models to ensure they are registered with Base
    from app.models.user import User  # noqa: F401
    
    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified successfully")


@retry_with_exponential_backoff()
@track_db_query_metrics("health_check")
async def check_database_connection() -> bool:
    """Check if database connection is healthy with retry logic."""
    try:
        engine = get_async_engine()
        start_time = time.time()
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Database connection is healthy (response time: {response_time:.2f}ms)")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


async def close_database_connections():
    """Close all database connections gracefully."""
    global async_engine, sync_engine
    try:
        if async_engine:
            await async_engine.dispose()
            async_engine = None
        if sync_engine:
            sync_engine.dispose()
            sync_engine = None
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")