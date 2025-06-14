"""
Application configuration settings using Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from typing import List
import secrets


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # App Information
    PROJECT_NAME: str = "Defeah Marketing Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # Authentication
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 128
    PASSWORD_STRENGTH_THRESHOLD: int = 60
    
    # Token Blacklisting
    TOKEN_BLACKLIST_TTL: int = 86400  # 24 hours in seconds
    
    # Rate Limiting
    LOGIN_RATE_LIMIT: int = 5  # attempts per minute
    LOGIN_RATE_WINDOW: int = 60  # seconds
    REGISTRATION_RATE_LIMIT: int = 3  # attempts per 5 minutes
    REGISTRATION_RATE_WINDOW: int = 300  # seconds
    GENERAL_RATE_LIMIT: int = 100  # requests per minute
    GENERAL_RATE_WINDOW: int = 60  # seconds
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5433/defeah_marketing"
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://postgres:password@localhost:5433/defeah_marketing"
    TEST_DATABASE_URL: str = "postgresql://postgres:password@localhost:5433/defeah_marketing_test"
    TEST_DATABASE_URL_ASYNC: str = "postgresql+asyncpg://postgres:password@localhost:5433/defeah_marketing_test"
    
    # Database Connection Configuration
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 30
    DB_POOL_RECYCLE: int = 3600  # 1 hour
    DB_POOL_PRE_PING: bool = True
    DB_CONNECT_TIMEOUT: int = 30  # seconds
    DB_COMMAND_TIMEOUT: int = 60  # seconds
    DB_SERVER_SIDE_CURSORS: bool = False
    
    # Database Retry Configuration
    DB_RETRY_ATTEMPTS: int = 3
    DB_RETRY_DELAY: float = 1.0  # Base delay in seconds
    DB_RETRY_BACKOFF: float = 2.0  # Exponential backoff multiplier
    DB_RETRY_MAX_DELAY: float = 60.0  # Maximum delay between retries
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 20
    REDIS_CONNECT_TIMEOUT: int = 5
    REDIS_SOCKET_TIMEOUT: int = 10
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React development server
        "http://localhost:3001",  # Alternative React port
        "http://localhost:8000",  # API server (for docs)
        "http://127.0.0.1:3000",  # IPv4 localhost
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000",
    ]
    
    # Additional CORS settings
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS: List[str] = [
        "Accept",
        "Accept-Language", 
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-CSRFToken",
        "X-API-Key"
    ]
    CORS_EXPOSE_HEADERS: List[str] = [
        "X-Error-ID",
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining", 
        "X-RateLimit-Reset",
        "Retry-After"
    ]
    CORS_MAX_AGE: int = 600  # 10 minutes

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()