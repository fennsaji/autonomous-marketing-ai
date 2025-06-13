"""
Application configuration settings using Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional
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
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5433/defeah_marketing"
    TEST_DATABASE_URL: str = "postgresql://postgres:password@localhost:5433/defeah_marketing_test"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Instagram/Facebook Integration
    FACEBOOK_APP_ID: str = ""
    FACEBOOK_APP_SECRET: str = ""
    INSTAGRAM_REDIRECT_URI: str = "http://localhost:3000/auth/instagram/callback"
    
    # OpenAI Integration
    OPENAI_API_KEY: str = ""
    
    # Rate Limiting
    REQUESTS_PER_MINUTE: int = 60
    MAX_POSTS_PER_DAY: int = 50
    
    # File Storage
    MEDIA_UPLOAD_PATH: str = "/tmp/uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Email Configuration (Optional)
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
    ]
    
    # Instagram API Configuration
    INSTAGRAM_BASE_URL: str = "https://graph.facebook.com/v18.0"
    INSTAGRAM_RATE_LIMIT: int = 200  # calls per hour per user
    
    # AI Content Generation Limits
    DAILY_AI_GENERATION_LIMIT: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()