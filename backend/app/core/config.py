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
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5433/defeah_marketing"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()