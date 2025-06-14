"""
Common schemas for API responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, Union


class ErrorDetail(BaseModel):
    """Error detail schema for standardized error responses."""
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    error_id: str = Field(..., description="Unique error identifier for tracking")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class ErrorResponse(BaseModel):
    """Standardized error response schema for all API errors."""
    error: ErrorDetail = Field(..., description="Error information")
    status: str = Field(default="error", description="Response status indicator")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "error_id": "123e4567-e89b-12d3-a456-426614174000",
                    "details": {
                        "validation_errors": {
                            "email": {
                                "message": "field required",
                                "type": "value_error.missing"
                            }
                        }
                    }
                },
                "status": "error"
            }
        }


class ValidationErrorDetail(BaseModel):
    """Validation error detail schema."""
    message: str = Field(..., description="Validation error message")
    type: str = Field(..., description="Validation error type")
    input: Optional[Any] = Field(None, description="Input value that caused the error")


class ValidationErrorResponse(BaseModel):
    """Validation error response schema."""
    error: ErrorDetail = Field(..., description="Validation error information")
    status: str = Field(default="error", description="Response status indicator")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "error_id": "123e4567-e89b-12d3-a456-426614174000",
                    "details": {
                        "validation_errors": {
                            "email": {
                                "message": "field required",
                                "type": "value_error.missing",
                                "input": None
                            }
                        },
                        "error_count": 1
                    }
                },
                "status": "error"
            }
        }


class SuccessResponse(BaseModel):
    """Standard success response schema."""
    message: str
    data: Optional[Any] = None


class ServiceStatus(BaseModel):
    """Service status schema for health checks."""
    status: str = Field(..., description="Service status: healthy, unhealthy, or not_configured")
    response_time_ms: float = Field(..., description="Response time in milliseconds")


class HealthResponse(BaseModel):
    """Enhanced health check response schema."""
    status: str = Field(..., description="Overall system status: healthy, degraded, or unhealthy")
    timestamp: Optional[str] = Field(None, description="ISO 8601 timestamp of the health check")
    version: Optional[str] = Field(None, description="Application version")
    environment: Optional[str] = Field(None, description="Environment name (development, staging, production)")
    services: Union[Dict[str, str], Dict[str, ServiceStatus]] = Field(
        ..., 
        description="Status of individual services"
    )
    response_time_ms: Optional[float] = Field(None, description="Total health check response time in milliseconds")


class HealthCheckResponse(BaseModel):
    """Simple health check response schema."""
    status: str
    message: str
    version: str


class RootResponse(BaseModel):
    """Root endpoint response schema."""
    message: str
    version: str
    environment: str
    docs_url: Optional[str] = None