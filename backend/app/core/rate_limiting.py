"""
Rate limiting middleware for authentication endpoints.
"""
import logging
from typing import Callable, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.redis_client import rate_limiter
from app.core.config import settings
from app.utils.exceptions import RateLimitError

logger = logging.getLogger(__name__)


def get_client_identifier(request: Request) -> str:
    """
    Get client identifier for rate limiting.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Client identifier string
    """
    # Try to get real IP from headers (for reverse proxy setups)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP in the chain
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else "unknown"
    
    return client_ip


class RateLimitMiddleware:
    """Rate limiting middleware for specific endpoints."""
    
    def __init__(self, calls: int, period: int, identifier_func: Callable = None):
        """
        Initialize rate limiter.
        
        Args:
            calls: Number of calls allowed
            period: Time period in seconds
            identifier_func: Function to get client identifier
        """
        self.calls = calls
        self.period = period
        self.identifier_func = identifier_func or get_client_identifier
    
    async def __call__(self, request: Request) -> Optional[JSONResponse]:
        """
        Check rate limit for request.
        
        Args:
            request: FastAPI request object
            
        Returns:
            JSONResponse if rate limited, None otherwise
        """
        try:
            identifier = self.identifier_func(request)
            endpoint = f"{request.method}:{request.url.path}"
            
            is_limited, info = await rate_limiter.is_rate_limited(
                identifier=identifier,
                limit=self.calls,
                window=self.period,
                action=endpoint
            )
            
            if is_limited:
                logger.warning(
                    "Rate limit exceeded for %s on %s: %d/%d requests",
                    identifier, endpoint, info.get("current_count", 0), self.calls
                )
                
                headers = {
                    "X-RateLimit-Limit": str(self.calls),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(info.get("reset_time", self.period)),
                    "Retry-After": str(info.get("retry_after", self.period))
                }
                
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Rate limit exceeded",
                        "error_code": "RATE_LIMIT_EXCEEDED",
                        "details": {
                            "limit": self.calls,
                            "window": self.period,
                            "retry_after": info.get("retry_after", self.period)
                        }
                    },
                    headers=headers
                )
            else:
                # Add rate limit headers for successful requests
                remaining = info.get("remaining", self.calls - 1)
                reset_time = info.get("reset_time", self.period)
                
                # Store rate limit info for response headers
                request.state.rate_limit_headers = {
                    "X-RateLimit-Limit": str(self.calls),
                    "X-RateLimit-Remaining": str(remaining),
                    "X-RateLimit-Reset": str(reset_time)
                }
                
                return None
                
        except Exception as e:
            logger.error("Error in rate limiting: %s", e)
            # Fail open - don't block requests if rate limiter fails
            return None


# Pre-configured rate limiters for different endpoints
login_rate_limiter = RateLimitMiddleware(
    calls=settings.LOGIN_RATE_LIMIT,
    period=settings.LOGIN_RATE_WINDOW
)

registration_rate_limiter = RateLimitMiddleware(
    calls=settings.REGISTRATION_RATE_LIMIT,
    period=settings.REGISTRATION_RATE_WINDOW
)

general_rate_limiter = RateLimitMiddleware(
    calls=settings.GENERAL_RATE_LIMIT,
    period=settings.GENERAL_RATE_WINDOW
)


def rate_limit(calls: int, period: int, identifier_func: Callable = None):
    """
    Decorator for applying rate limiting to FastAPI endpoints.
    
    Args:
        calls: Number of calls allowed
        period: Time period in seconds
        identifier_func: Function to get client identifier
        
    Returns:
        Decorator function
    """
    limiter = RateLimitMiddleware(calls, period, identifier_func)
    
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract request from args or kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                # Look in kwargs
                request = kwargs.get("request")
            
            if request:
                # Check rate limit
                response = await limiter(request)
                if response:
                    return response
            
            # Execute original function
            result = await func(*args, **kwargs)
            
            # Add rate limit headers to response if available
            if (request and hasattr(request.state, "rate_limit_headers") 
                and hasattr(result, "headers")):
                for key, value in request.state.rate_limit_headers.items():
                    result.headers[key] = value
            
            return result
        
        return wrapper
    return decorator


async def check_authentication_rate_limit(request: Request, action: str) -> bool:
    """
    Check rate limit for authentication actions.
    
    Args:
        request: FastAPI request object
        action: Action type ("login", "registration", etc.)
        
    Returns:
        True if allowed, False if rate limited
        
    Raises:
        RateLimitError: If rate limit exceeded
    """
    identifier = get_client_identifier(request)
    
    if action == "login":
        limit = settings.LOGIN_RATE_LIMIT
        window = settings.LOGIN_RATE_WINDOW
    elif action == "registration":
        limit = settings.REGISTRATION_RATE_LIMIT
        window = settings.REGISTRATION_RATE_WINDOW
    else:
        limit = settings.GENERAL_RATE_LIMIT
        window = settings.GENERAL_RATE_WINDOW
    
    try:
        is_limited, info = await rate_limiter.is_rate_limited(
            identifier=identifier,
            limit=limit,
            window=window,
            action=action
        )
        
        if is_limited:
            raise RateLimitError(
                message=f"Too many {action} attempts",
                retry_after=info.get("retry_after"),
                limit=limit,
                window=window
            )
        
        return True
        
    except RateLimitError:
        raise
    except Exception as e:
        logger.error("Error checking authentication rate limit: %s", e)
        # Fail open - allow request if rate limiter fails
        return True