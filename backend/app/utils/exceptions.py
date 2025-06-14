"""
Custom exceptions and error handling utilities.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional, Dict, Any
import logging
import uuid

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
    """Setup comprehensive global exception handlers for consistent error responses."""
    
    @app.exception_handler(BaseAPIException)
    async def api_exception_handler(request: Request, exc: BaseAPIException):
        """Handle custom API exceptions with detailed error information."""
        error_id = str(uuid.uuid4())
        
        logger.error(
            "API Exception [%s]: %s (Code: %s) - Path: %s %s", 
            error_id, exc.message, exc.error_code, request.method, request.url.path
        )
        
        response_content = {
            "error": {
                "code": exc.error_code or "API_ERROR",
                "message": exc.message,
                "error_id": error_id
            },
            "status": "error"
        }
        
        # Add details if available
        if exc.details:
            response_content["error"]["details"] = exc.details
        
        # Add retry-after header for rate limiting
        headers = {"X-Error-ID": error_id}
        if isinstance(exc, RateLimitError) and exc.details and exc.details.get("retry_after"):
            headers["Retry-After"] = str(exc.details["retry_after"])
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response_content,
            headers=headers
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic request validation errors with field-specific details."""
        error_id = str(uuid.uuid4())
        
        logger.warning(
            "Validation Error [%s]: %s - Path: %s %s", 
            error_id, str(exc), request.method, request.url.path
        )
        
        # Format validation errors
        validation_errors = {}
        for error in exc.errors():
            field_path = ".".join(str(x) for x in error["loc"])
            validation_errors[field_path] = {
                "message": error["msg"],
                "type": error["type"],
                "input": error.get("input")
            }
        
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "error_id": error_id,
                    "details": {
                        "validation_errors": validation_errors,
                        "error_count": len(exc.errors())
                    }
                },
                "status": "error"
            },
            headers={"X-Error-ID": error_id}
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        """Handle Pydantic model validation errors."""
        error_id = str(uuid.uuid4())
        
        logger.warning(
            "Pydantic Validation Error [%s]: %s - Path: %s %s", 
            error_id, str(exc), request.method, request.url.path
        )
        
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "MODEL_VALIDATION_ERROR",
                    "message": "Data validation failed",
                    "error_id": error_id,
                    "details": {
                        "validation_errors": exc.errors()
                    }
                },
                "status": "error"
            },
            headers={"X-Error-ID": error_id}
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle FastAPI HTTP exceptions with standardized format."""
        error_id = str(uuid.uuid4())
        
        logger.warning(
            "HTTP Exception [%s]: %s (Status: %d) - Path: %s %s", 
            error_id, exc.detail, exc.status_code, request.method, request.url.path
        )
        
        # Map common HTTP status codes to error codes
        error_code_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED", 
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            409: "CONFLICT",
            410: "GONE",
            429: "RATE_LIMIT_EXCEEDED",
            500: "INTERNAL_SERVER_ERROR",
            502: "BAD_GATEWAY",
            503: "SERVICE_UNAVAILABLE",
            504: "GATEWAY_TIMEOUT"
        }
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": error_code_map.get(exc.status_code, "HTTP_ERROR"),
                    "message": exc.detail,
                    "error_id": error_id
                },
                "status": "error"
            },
            headers={"X-Error-ID": error_id}
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle Starlette HTTP exceptions."""
        error_id = str(uuid.uuid4())
        
        logger.warning(
            "Starlette HTTP Exception [%s]: %s (Status: %d) - Path: %s %s", 
            error_id, exc.detail, exc.status_code, request.method, request.url.path
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": "HTTP_ERROR",
                    "message": exc.detail,
                    "error_id": error_id
                },
                "status": "error"
            },
            headers={"X-Error-ID": error_id}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions with secure error information."""
        error_id = str(uuid.uuid4())
        
        logger.error(
            "Unhandled Exception [%s]: %s - Path: %s %s", 
            error_id, str(exc), request.method, request.url.path, 
            exc_info=True
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. Please try again later.",
                    "error_id": error_id
                },
                "status": "error"
            },
            headers={"X-Error-ID": error_id}
        )