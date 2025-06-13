"""
Custom exceptions and error handlers.
"""
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
import logging

logger = logging.getLogger(__name__)


# Custom exceptions
class BaseCustomException(HTTPException):
    """Base custom exception."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExistsException(BaseCustomException):
    """Exception raised when user already exists."""
    def __init__(self, detail: str = "User already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class InvalidCredentialsException(BaseCustomException):
    """Exception raised for invalid credentials."""
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class InstagramAPIException(BaseCustomException):
    """Exception raised for Instagram API errors."""
    def __init__(self, detail: str = "Instagram API error"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class OpenAIAPIException(BaseCustomException):
    """Exception raised for OpenAI API errors."""
    def __init__(self, detail: str = "AI service error"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RateLimitException(BaseCustomException):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, detail: str = "Rate limit exceeded", retry_after: int = 3600):
        super().__init__(detail=detail, status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        self.retry_after = retry_after


class PostNotFoundException(BaseCustomException):
    """Exception raised when post is not found."""
    def __init__(self, detail: str = "Post not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class CampaignNotFoundException(BaseCustomException):
    """Exception raised when campaign is not found."""
    def __init__(self, detail: str = "Campaign not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class InsufficientPermissionsException(BaseCustomException):
    """Exception raised for insufficient permissions."""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class ValidationException(BaseCustomException):
    """Exception raised for validation errors."""
    def __init__(self, detail: str = "Validation error", errors: list = None):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.errors = errors or []


# Error response models
def create_error_response(
    error_code: str,
    detail: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    errors: list = None,
    retry_after: int = None
) -> dict:
    """Create standardized error response."""
    response = {
        "detail": detail,
        "error_code": error_code
    }
    
    if errors:
        response["errors"] = errors
    
    if retry_after:
        response["retry_after"] = retry_after
    
    return response


# Exception handlers
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    
    # Log the error
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    # Map common HTTP errors to custom error codes
    error_code_map = {
        status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
        status.HTTP_403_FORBIDDEN: "FORBIDDEN", 
        status.HTTP_404_NOT_FOUND: "NOT_FOUND",
        status.HTTP_409_CONFLICT: "CONFLICT",
        status.HTTP_422_UNPROCESSABLE_ENTITY: "VALIDATION_ERROR",
        status.HTTP_429_TOO_MANY_REQUESTS: "RATE_LIMIT_EXCEEDED",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "INTERNAL_ERROR"
    }
    
    error_code = error_code_map.get(exc.status_code, "UNKNOWN_ERROR")
    
    response_data = create_error_response(
        error_code=error_code,
        detail=exc.detail,
        status_code=exc.status_code
    )
    
    # Add retry_after header for rate limiting
    headers = getattr(exc, 'headers', None)
    if exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        if hasattr(exc, 'retry_after'):
            response_data["retry_after"] = exc.retry_after
            headers = {"Retry-After": str(exc.retry_after)}
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data,
        headers=headers
    )


async def validation_exception_handler(request: Request, exc: ValidationException):
    """Handle validation exceptions."""
    response_data = create_error_response(
        error_code="VALIDATION_ERROR",
        detail=exc.detail,
        status_code=exc.status_code,
        errors=exc.errors
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.exception(f"Unexpected error: {str(exc)}")
    
    response_data = create_error_response(
        error_code="INTERNAL_ERROR",
        detail="An unexpected error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_data
    )


def setup_exception_handlers(app):
    """Setup all exception handlers for the FastAPI app."""
    
    # Custom exception handlers
    app.add_exception_handler(HTTPException, custom_http_exception_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Specific custom exceptions
    app.add_exception_handler(UserAlreadyExistsException, custom_http_exception_handler)
    app.add_exception_handler(InvalidCredentialsException, custom_http_exception_handler)
    app.add_exception_handler(InstagramAPIException, custom_http_exception_handler)
    app.add_exception_handler(OpenAIAPIException, custom_http_exception_handler)
    app.add_exception_handler(RateLimitException, custom_http_exception_handler)
    app.add_exception_handler(PostNotFoundException, custom_http_exception_handler)
    app.add_exception_handler(CampaignNotFoundException, custom_http_exception_handler)
    app.add_exception_handler(InsufficientPermissionsException, custom_http_exception_handler)