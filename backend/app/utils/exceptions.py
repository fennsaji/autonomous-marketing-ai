"""
Custom exceptions and error handling utilities.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseAPIException(Exception):
    """Base API exception class."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500, 
        error_code: str = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(BaseAPIException):
    """Exception for validation errors."""
    
    def __init__(self, message: str, field: str = None):
        details = {"field": field} if field else {}
        super().__init__(message, 400, "VALIDATION_ERROR", details)


class DatabaseException(BaseAPIException):
    """Exception for database errors."""
    
    def __init__(self, message: str):
        super().__init__(message, 500, "DATABASE_ERROR")


# Authentication Exceptions
class AuthenticationError(BaseAPIException):
    """Base class for authentication-related errors."""
    
    def __init__(self, message: str, status_code: int = 401, error_code: str = None):
        super().__init__(message, status_code, error_code or "AUTHENTICATION_ERROR")


class InvalidCredentialsError(AuthenticationError):
    """Raised when user credentials are invalid."""
    
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message, 401, "INVALID_CREDENTIALS")


class TokenExpiredError(AuthenticationError):
    """Raised when JWT token has expired."""
    
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, 401, "TOKEN_EXPIRED")


class TokenInvalidError(AuthenticationError):
    """Raised when JWT token is invalid or malformed."""
    
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message, 401, "TOKEN_INVALID")


class TokenBlacklistedError(AuthenticationError):
    """Raised when JWT token is blacklisted."""
    
    def __init__(self, message: str = "Token has been revoked"):
        super().__init__(message, 401, "TOKEN_BLACKLISTED")


class AccountInactiveError(AuthenticationError):
    """Raised when user account is inactive."""
    
    def __init__(self, message: str = "User account is inactive"):
        super().__init__(message, 401, "ACCOUNT_INACTIVE")


class EmailNotVerifiedError(AuthenticationError):
    """Raised when user email is not verified."""
    
    def __init__(self, message: str = "Email verification required"):
        super().__init__(message, 403, "EMAIL_NOT_VERIFIED")


class AccountLockedError(AuthenticationError):
    """Raised when user account is temporarily locked."""
    
    def __init__(self, message: str = "Account temporarily locked", unlock_time: int = None):
        details = {"unlock_time": unlock_time} if unlock_time else {}
        super().__init__(message, 423, "ACCOUNT_LOCKED")
        self.details = details


# User Management Exceptions
class UserNotFoundError(BaseAPIException):
    """Raised when user is not found."""
    
    def __init__(self, message: str = "User not found"):
        super().__init__(message, 404, "USER_NOT_FOUND")


class UserAlreadyExistsError(BaseAPIException):
    """Raised when attempting to create a user that already exists."""
    
    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message, 409, "USER_ALREADY_EXISTS")


class PasswordTooWeakError(BaseAPIException):
    """Raised when password doesn't meet strength requirements."""
    
    def __init__(self, message: str, requirements: Optional[Dict[str, Any]] = None):
        details = {"requirements": requirements} if requirements else {}
        super().__init__(message, 400, "PASSWORD_TOO_WEAK", details)


# Rate Limiting Exceptions
class RateLimitError(BaseAPIException):
    """Raised when rate limit is exceeded."""
    
    def __init__(
        self, 
        message: str = "Rate limit exceeded", 
        retry_after: int = None,
        limit: int = None,
        window: int = None
    ):
        details = {}
        if retry_after:
            details["retry_after"] = retry_after
        if limit:
            details["limit"] = limit
        if window:
            details["window"] = window
            
        super().__init__(message, 429, "RATE_LIMIT_EXCEEDED", details)


# Service Exceptions
class RedisConnectionError(BaseAPIException):
    """Raised when Redis connection fails."""
    
    def __init__(self, message: str = "Redis connection failed"):
        super().__init__(message, 503, "REDIS_CONNECTION_ERROR")


def setup_exception_handlers(app: FastAPI):
    """Setup global exception handlers."""
    
    @app.exception_handler(BaseAPIException)
    async def api_exception_handler(request: Request, exc: BaseAPIException):
        """Handle custom API exceptions."""
        logger.error("API Exception: %s (Code: %s)", exc.message, exc.error_code)
        
        response_content = {
            "detail": exc.message,
            "error_code": exc.error_code
        }
        
        # Add details if available
        if exc.details:
            response_content["details"] = exc.details
        
        # Add retry-after header for rate limiting
        headers = {}
        if isinstance(exc, RateLimitError) and exc.details.get("retry_after"):
            headers["Retry-After"] = str(exc.details["retry_after"])
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response_content,
            headers=headers if headers else None
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        logger.error("HTTP Exception: %s", exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error("Unhandled exception: %s", str(exc), exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error_code": "INTERNAL_SERVER_ERROR"
            }
        )