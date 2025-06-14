"""
Common schemas for API responses.
"""
from pydantic import BaseModel
from typing import Optional, Any, Dict


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    detail: str
    error_code: Optional[str] = None
    errors: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    """Standard success response schema."""
    message: str
    data: Optional[Any] = None


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    services: Dict[str, str]


class RootResponse(BaseModel):
    """Root endpoint response schema."""
    message: str
    version: str
    environment: str
    docs_url: Optional[str] = None