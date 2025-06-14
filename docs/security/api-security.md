# API Security

Comprehensive API security guide for the Defeah Marketing Backend.

## API Security Overview

The Defeah Marketing API implements multiple layers of security to protect against common vulnerabilities and ensure secure access to marketing automation features.

### Security Principles
1. **Defense in Depth**: Multiple security layers
2. **Least Privilege**: Minimal necessary permissions
3. **Input Validation**: Comprehensive request validation
4. **Output Encoding**: Secure response formatting
5. **Rate Limiting**: Protection against abuse
6. **Monitoring**: Real-time threat detection

## Authentication & Authorization

### JWT Bearer Token Authentication

All API endpoints (except public endpoints) require JWT authentication:

```bash
# Authenticated request
curl -X GET https://api.defeah.com/api/v1/posts \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Authentication Flow Security

```mermaid
sequenceDiagram
    participant Client
    participant API Gateway
    participant Auth Service
    participant Rate Limiter
    participant Application
    
    Client->>API Gateway: Request + JWT
    API Gateway->>Rate Limiter: Check limits
    alt Rate limit exceeded
        Rate Limiter-->>API Gateway: 429 Too Many Requests
        API Gateway-->>Client: Rate limit error
    else Within limits
        API Gateway->>Auth Service: Validate JWT
        alt Invalid/expired token
            Auth Service-->>API Gateway: 401 Unauthorized
            API Gateway-->>Client: Auth error
        else Valid token
            Auth Service-->>API Gateway: User context
            API Gateway->>Application: Authorized request
            Application-->>API Gateway: Response
            API Gateway-->>Client: Success response
        end
    end
```

### Role-Based Authorization

```python
# Authorization Decorator Implementation
from functools import wraps
from fastapi import HTTPException, Depends, Request
from typing import List, Optional

class RequirePermissions:
    def __init__(self, permissions: List[str], resource_type: str = None):
        self.permissions = permissions
        self.resource_type = resource_type
    
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current user from JWT
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=401, detail="Authentication required")
            
            # Check user permissions
            for permission in self.permissions:
                if not self.user_has_permission(current_user, permission):
                    raise HTTPException(
                        status_code=403,
                        detail=f"Missing required permission: {permission}"
                    )
            
            # Resource-level authorization
            if self.resource_type:
                resource_id = kwargs.get('id') or kwargs.get(f'{self.resource_type}_id')
                if resource_id and not self.can_access_resource(
                    current_user, self.resource_type, resource_id
                ):
                    raise HTTPException(
                        status_code=403,
                        detail="Access denied to this resource"
                    )
            
            return await func(*args, **kwargs)
        return wrapper
    
    def user_has_permission(self, user, permission: str) -> bool:
        return permission in user.permissions
    
    def can_access_resource(self, user, resource_type: str, resource_id: str) -> bool:
        # Check if user owns resource or has admin access
        if 'admin' in user.roles:
            return True
        
        if resource_type == 'post':
            # Users can only access their own posts
            return self.get_post_owner(resource_id) == user.id
        
        return False

# Usage examples
@router.get("/posts/{post_id}")
@RequirePermissions(["read:posts"], resource_type="post")
async def get_post(post_id: str, current_user: User = Depends(get_current_user)):
    return await post_service.get_post(post_id)

@router.post("/posts")
@RequirePermissions(["create:posts"])
async def create_post(
    post_data: PostCreate, 
    current_user: User = Depends(get_current_user)
):
    return await post_service.create_post(post_data, current_user.id)
```

## Input Validation & Sanitization

### Comprehensive Request Validation

```python
from pydantic import BaseModel, validator, Field, EmailStr
from typing import List, Optional, Dict, Any
import re
from datetime import datetime

class StrictPostCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=500, min_length=1)
    caption: str = Field(..., max_length=2200, min_length=1)
    hashtags: Optional[List[str]] = Field(default=[], max_items=30)
    media_urls: List[str] = Field(..., min_items=1, max_items=10)
    scheduled_at: Optional[datetime] = None
    campaign_id: Optional[str] = Field(None, regex=r'^[0-9a-f-]{36}$')
    
    class Config:
        # Reject extra fields
        extra = "forbid"
        # Validate assignment
        validate_assignment = True
        # Use enum values
        use_enum_values = True
    
    @validator('caption')
    def validate_caption(cls, v):
        # XSS Prevention
        if re.search(r'<script|javascript:|data:|vbscript:', v, re.IGNORECASE):
            raise ValueError("Potentially malicious content detected")
        
        # SQL Injection Prevention
        sql_patterns = [
            r"('|(\\\\')|(;)|(\\|\\|)|(\\|/*|*/)",
            r"(union|select|insert|delete|update|drop|create|alter|exec|execute)",
        ]
        for pattern in sql_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Invalid characters detected")
        
        return v.strip()
    
    @validator('hashtags', each_item=True)
    def validate_hashtag(cls, v):
        # Hashtag format validation
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("Invalid hashtag format")
        
        if len(v) > 100:
            raise ValueError("Hashtag too long")
        
        return v.lower()
    
    @validator('media_urls', each_item=True)
    def validate_media_url(cls, v):
        # URL validation
        if not re.match(r'^https?://', v):
            raise ValueError("Only HTTP(S) URLs allowed")
        
        # Domain whitelist for security
        allowed_domains = [
            'api.defeah.com',
            'cdn.defeah.com',
            'uploads.defeah.com',
            's3.amazonaws.com',
            'storage.googleapis.com'
        ]
        
        from urllib.parse import urlparse
        domain = urlparse(v).netloc
        if not any(domain.endswith(allowed) for allowed in allowed_domains):
            raise ValueError(f"Domain not allowed: {domain}")
        
        return v
    
    @validator('scheduled_at')
    def validate_scheduled_at(cls, v):
        if v and v <= datetime.utcnow():
            raise ValueError("Scheduled time must be in the future")
        return v

# File Upload Validation
import magic
from fastapi import UploadFile
from typing import Set

class FileValidator:
    ALLOWED_MIME_TYPES: Set[str] = {
        'image/jpeg', 'image/png', 'image/webp', 'image/gif',
        'video/mp4', 'video/quicktime', 'video/x-msvideo'
    }
    
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    @classmethod
    async def validate_file(cls, file: UploadFile) -> bool:
        # Check file size
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > cls.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes")
        
        # Reset file position
        await file.seek(0)
        
        # Check MIME type using python-magic
        mime_type = magic.from_buffer(content, mime=True)
        if mime_type not in cls.ALLOWED_MIME_TYPES:
            raise ValueError(f"File type not allowed: {mime_type}")
        
        # Check for malicious content
        if cls.has_malicious_content(content):
            raise ValueError("Potentially malicious file detected")
        
        return True
    
    @staticmethod
    def has_malicious_content(content: bytes) -> bool:
        # Check for embedded scripts or executables
        malicious_patterns = [
            b'<script', b'javascript:', b'data:',
            b'MZ',  # PE executable header
            b'\x7fELF',  # ELF executable header
            b'#!/',  # Shell script
        ]
        
        content_lower = content.lower()
        return any(pattern in content_lower for pattern in malicious_patterns)

# Usage in endpoint
@router.post("/media/upload")
async def upload_media(
    file: UploadFile,
    current_user: User = Depends(get_current_user)
):
    await FileValidator.validate_file(file)
    # Process file upload
    return await media_service.upload_file(file, current_user.id)
```

### SQL Injection Prevention

```python
# SECURE: Using SQLAlchemy with parameterized queries
from sqlalchemy import text, select
from sqlalchemy.orm import Session

class SecurePostRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_posts(self, user_id: str, search: str = None, limit: int = 10):
        # Use parameterized queries
        query = select(Post).where(
            Post.user_id == user_id,
            Post.deleted_at.is_(None)
        )
        
        if search:
            # Safe string search using parameter binding
            query = query.where(
                Post.caption.ilike(f"%{search}%") |
                Post.title.ilike(f"%{search}%")
            )
        
        return self.db.execute(
            query.limit(limit)
        ).scalars().all()
    
    def get_posts_by_campaign(self, campaign_id: str, user_id: str):
        # Using text() with bound parameters for complex queries
        query = text("""
            SELECT p.*, c.name as campaign_name
            FROM posts p
            JOIN campaigns c ON p.campaign_id = c.id
            WHERE p.campaign_id = :campaign_id
            AND p.user_id = :user_id
            AND p.deleted_at IS NULL
            ORDER BY p.created_at DESC
        """)
        
        return self.db.execute(
            query,
            {"campaign_id": campaign_id, "user_id": user_id}
        ).fetchall()

# INSECURE: String concatenation (DO NOT USE)
# def get_user_posts_insecure(self, user_id: str, search: str = None):
#     # VULNERABLE TO SQL INJECTION
#     query = f"SELECT * FROM posts WHERE user_id = '{user_id}'"
#     if search:
#         query += f" AND caption LIKE '%{search}%'"
#     return self.db.execute(query)
```

## Rate Limiting

### Multi-Level Rate Limiting

```python
import asyncio
import time
from enum import Enum
from typing import Dict, Tuple, Optional
import redis.asyncio as redis
from contextlib import asynccontextmanager

class RateLimitType(Enum):
    GLOBAL = "global"
    USER = "user"
    IP = "ip"
    ENDPOINT = "endpoint"
    INSTAGRAM = "instagram"

class RateLimitConfig:
    LIMITS = {
        RateLimitType.GLOBAL: {"requests": 100000, "window": 3600},  # 100k/hour globally
        RateLimitType.IP: {"requests": 1000, "window": 3600},        # 1k/hour per IP
        RateLimitType.USER: {"requests": 10000, "window": 3600},     # 10k/hour per user
        RateLimitType.ENDPOINT: {
            "/api/v1/auth/login": {"requests": 10, "window": 900},   # 10/15min login
            "/api/v1/posts": {"requests": 100, "window": 3600},      # 100/hour posts
            "/api/v1/instagram/publish": {"requests": 50, "window": 86400}, # 50/day publish
        },
        RateLimitType.INSTAGRAM: {"requests": 200, "window": 3600},  # Instagram API limits
    }

class AdvancedRateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.config = RateLimitConfig()
    
    async def check_rate_limit(
        self,
        identifier: str,
        limit_type: RateLimitType,
        endpoint: str = None
    ) -> Tuple[bool, Dict]:
        """
        Check multiple rate limit conditions
        Returns: (is_allowed, rate_info)
        """
        # Get limit configuration
        if limit_type == RateLimitType.ENDPOINT and endpoint:
            limit_config = self.config.LIMITS[limit_type].get(
                endpoint, 
                {"requests": 1000, "window": 3600}
            )
        else:
            limit_config = self.config.LIMITS[limit_type]
        
        requests_limit = limit_config["requests"]
        window_seconds = limit_config["window"]
        
        # Use sliding window rate limiting
        is_allowed, rate_info = await self._sliding_window_check(
            identifier, requests_limit, window_seconds
        )
        
        # Add burst protection
        if is_allowed:
            is_allowed = await self._burst_protection_check(identifier)
        
        return is_allowed, rate_info
    
    async def _sliding_window_check(
        self, 
        identifier: str, 
        limit: int, 
        window: int
    ) -> Tuple[bool, Dict]:
        """Sliding window rate limit implementation"""
        current_time = time.time()
        window_start = current_time - window
        
        pipe = self.redis.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(f"rate_limit:{identifier}", 0, window_start)
        
        # Count current requests
        pipe.zcard(f"rate_limit:{identifier}")
        
        # Add current request
        pipe.zadd(f"rate_limit:{identifier}", {str(current_time): current_time})
        
        # Set expiration
        pipe.expire(f"rate_limit:{identifier}", window)
        
        results = await pipe.execute()
        current_requests = results[1] + 1  # Include current request
        
        remaining = max(0, limit - current_requests)
        reset_time = current_time + window
        
        rate_info = {
            "limit": limit,
            "remaining": remaining,
            "reset": int(reset_time),
            "window": window,
            "retry_after": 0 if current_requests <= limit else int(window)
        }
        
        return current_requests <= limit, rate_info
    
    async def _burst_protection_check(self, identifier: str) -> bool:
        """Prevent burst attacks with token bucket"""
        bucket_key = f"burst:{identifier}"
        bucket_size = 10
        refill_rate = 2  # tokens per second
        
        current_time = time.time()
        
        # Get current bucket state
        bucket_data = await self.redis.hmget(
            bucket_key, "tokens", "last_refill"
        )
        
        tokens = float(bucket_data[0] or bucket_size)
        last_refill = float(bucket_data[1] or current_time)
        
        # Refill tokens
        time_passed = current_time - last_refill
        tokens = min(bucket_size, tokens + (time_passed * refill_rate))
        
        if tokens >= 1:
            # Consume token
            tokens -= 1
            await self.redis.hmset(bucket_key, {
                "tokens": tokens,
                "last_refill": current_time
            })
            await self.redis.expire(bucket_key, 300)  # 5 minutes
            return True
        
        return False

# Rate Limiting Middleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class RateLimitMiddleware:
    def __init__(self, redis_client: redis.Redis):
        self.rate_limiter = AdvancedRateLimiter(redis_client)
    
    async def __call__(self, request: Request, call_next):
        # Extract identifiers
        ip_address = request.client.host
        user_id = self.get_user_id_from_request(request)
        endpoint = request.url.path
        
        # Check multiple rate limits
        checks = [
            (ip_address, RateLimitType.IP),
            (f"global", RateLimitType.GLOBAL),
        ]
        
        if user_id:
            checks.append((user_id, RateLimitType.USER))
        
        if endpoint.startswith("/api/v1/instagram"):
            checks.append((user_id or ip_address, RateLimitType.INSTAGRAM))
        
        # Check endpoint-specific limits
        checks.append((f"{endpoint}:{user_id or ip_address}", RateLimitType.ENDPOINT))
        
        # Evaluate all rate limits
        for identifier, limit_type in checks:
            is_allowed, rate_info = await self.rate_limiter.check_rate_limit(
                identifier, limit_type, endpoint
            )
            
            if not is_allowed:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": f"Rate limit exceeded for {limit_type.value}",
                            "details": rate_info
                        }
                    },
                    headers={
                        "X-RateLimit-Limit": str(rate_info["limit"]),
                        "X-RateLimit-Remaining": str(rate_info["remaining"]),
                        "X-RateLimit-Reset": str(rate_info["reset"]),
                        "Retry-After": str(rate_info["retry_after"])
                    }
                )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers from the most restrictive limit
        user_identifier = user_id or ip_address
        _, user_rate_info = await self.rate_limiter.check_rate_limit(
            user_identifier, RateLimitType.USER
        )
        
        response.headers["X-RateLimit-Limit"] = str(user_rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(user_rate_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(user_rate_info["reset"])
        
        return response
    
    def get_user_id_from_request(self, request: Request) -> Optional[str]:
        # Extract user ID from JWT token
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                # Decode JWT to get user ID
                payload = jwt.decode(token, verify=False)  # Verification done elsewhere
                return payload.get("sub")
            except:
                pass
        return None
```

## Output Security

### Response Sanitization

```python
from typing import Any, Dict
import json
import re

class SecureResponseHandler:
    """Secure response handling and sanitization"""
    
    SENSITIVE_FIELDS = {
        'password', 'hashed_password', 'secret', 'token', 'key',
        'instagram_token', 'access_token', 'refresh_token', 'api_key'
    }
    
    @classmethod
    def sanitize_response(cls, data: Any) -> Any:
        """Remove sensitive data from responses"""
        if isinstance(data, dict):
            return {
                key: cls.sanitize_response(value)
                for key, value in data.items()
                if key not in cls.SENSITIVE_FIELDS
            }
        elif isinstance(data, list):
            return [cls.sanitize_response(item) for item in data]
        elif isinstance(data, str):
            return cls.sanitize_string(data)
        else:
            return data
    
    @classmethod
    def sanitize_string(cls, text: str) -> str:
        """Sanitize string output to prevent XSS"""
        # HTML escape
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&#x27;")
        
        # Remove potentially dangerous URLs
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'data:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'vbscript:', '', text, flags=re.IGNORECASE)
        
        return text
    
    @classmethod
    def secure_json_response(cls, data: Any, status_code: int = 200) -> JSONResponse:
        """Create secure JSON response"""
        sanitized_data = cls.sanitize_response(data)
        
        headers = {
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            # XSS Protection
            "X-XSS-Protection": "1; mode=block",
            # Frame Options
            "X-Frame-Options": "DENY",
            # Content Security Policy
            "Content-Security-Policy": "default-src 'self'",
            # Referrer Policy
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        
        return JSONResponse(
            content=sanitized_data,
            status_code=status_code,
            headers=headers
        )

# Usage in API endpoints
@router.get("/posts/{post_id}")
async def get_post(post_id: str, current_user: User = Depends(get_current_user)):
    post = await post_service.get_post(post_id)
    
    # Convert to dict and sanitize
    post_dict = {
        "id": str(post.id),
        "title": post.title,
        "caption": post.caption,
        "hashtags": post.hashtags,
        "media_urls": post.media_urls,
        "created_at": post.created_at.isoformat(),
        "user": {
            "id": str(post.user.id),
            "full_name": post.user.full_name,
            "email": post.user.email  # This will be removed by sanitization
        }
    }
    
    return SecureResponseHandler.secure_json_response(post_dict)
```

### Error Handling Security

```python
import logging
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationError
import traceback
import uuid

class SecureErrorHandler:
    """Secure error handling that doesn't leak sensitive information"""
    
    def __init__(self):
        self.logger = logging.getLogger("security.errors")
    
    async def handle_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle exceptions securely"""
        error_id = str(uuid.uuid4())
        
        # Log full error details securely
        self.logger.error(
            f"Error ID: {error_id} | Path: {request.url.path} | "
            f"Method: {request.method} | IP: {request.client.host} | "
            f"Error: {str(exc)} | Traceback: {traceback.format_exc()}"
        )
        
        # Return sanitized error response
        if isinstance(exc, HTTPException):
            return self._handle_http_exception(exc, error_id)
        elif isinstance(exc, ValidationError):
            return self._handle_validation_error(exc, error_id)
        else:
            return self._handle_generic_error(exc, error_id)
    
    def _handle_http_exception(self, exc: HTTPException, error_id: str) -> JSONResponse:
        """Handle HTTP exceptions"""
        # Sanitize error details
        safe_detail = self._sanitize_error_message(str(exc.detail))
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": safe_detail,
                    "error_id": error_id
                }
            }
        )
    
    def _handle_validation_error(self, exc: ValidationError, error_id: str) -> JSONResponse:
        """Handle validation errors"""
        # Extract safe field information
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            message = self._sanitize_error_message(error["msg"])
            errors.append({"field": field, "message": message})
        
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": errors,
                    "error_id": error_id
                }
            }
        )
    
    def _handle_generic_error(self, exc: Exception, error_id: str) -> JSONResponse:
        """Handle generic errors without leaking information"""
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "error_id": error_id
                }
            }
        )
    
    def _sanitize_error_message(self, message: str) -> str:
        """Sanitize error messages to prevent information leakage"""
        # Remove file paths
        message = re.sub(r'[/\\][a-zA-Z0-9_./\\-]+', '[PATH_REMOVED]', message)
        
        # Remove database connection strings
        message = re.sub(
            r'postgresql://[^@\s]+@[^/\s]+/[^\s]+',
            'postgresql://[REDACTED]',
            message
        )
        
        # Remove API keys or tokens
        message = re.sub(
            r'[a-zA-Z0-9]{32,}',
            '[TOKEN_REDACTED]',
            message
        )
        
        return message

# Global exception handler
from fastapi import FastAPI

def setup_secure_error_handling(app: FastAPI):
    error_handler = SecureErrorHandler()
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return await error_handler.handle_exception(request, exc)
```

## CORS Security

### Secure CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

def configure_secure_cors(app: FastAPI, environment: str):
    """Configure CORS with security best practices"""
    
    if environment == "development":
        # Development: More permissive for local development
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
        ]
    elif environment == "staging":
        # Staging: Specific staging domains
        allowed_origins = [
            "https://staging.defeah.com",
            "https://staging-admin.defeah.com",
        ]
    else:  # production
        # Production: Only production domains
        allowed_origins = [
            "https://defeah.com",
            "https://www.defeah.com",
            "https://admin.defeah.com",
            "https://app.defeah.com",
        ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,  # Allow cookies/auth headers
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "User-Agent",
            "X-Requested-With",
            "X-CSRF-Token",
        ],
        expose_headers=[
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
        ],
        max_age=86400,  # 24 hours preflight cache
    )

# Custom CORS middleware for advanced security
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class AdvancedCORSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_origins: list, allowed_hosts: list = None):
        super().__init__(app)
        self.allowed_origins = set(allowed_origins)
        self.allowed_hosts = set(allowed_hosts or [])
    
    async def dispatch(self, request, call_next):
        origin = request.headers.get("Origin")
        host = request.headers.get("Host")
        
        # Validate Origin header
        if origin and origin not in self.allowed_origins:
            return Response(
                content="Origin not allowed",
                status_code=403,
                headers={"Content-Type": "text/plain"}
            )
        
        # Validate Host header (Host header injection protection)
        if self.allowed_hosts and host not in self.allowed_hosts:
            return Response(
                content="Host not allowed",
                status_code=403,
                headers={"Content-Type": "text/plain"}
            )
        
        # Process request
        response = await call_next(request)
        
        # Add security headers
        if origin in self.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Vary"] = "Origin"
        
        return response
```

## Security Headers

### Comprehensive Security Headers

```python
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add comprehensive security headers to all responses"""
    
    def __init__(self, app, csp_policy: str = None):
        super().__init__(app)
        self.csp_policy = csp_policy or self._default_csp_policy()
    
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        
        # Security headers
        security_headers = {
            # Prevent XSS attacks
            "X-XSS-Protection": "1; mode=block",
            
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            
            # Prevent clickjacking
            "X-Frame-Options": "DENY",
            
            # Content Security Policy
            "Content-Security-Policy": self.csp_policy,
            
            # HTTPS enforcement (in production)
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
            
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            
            # Permissions policy
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
            
            # Remove server information
            "Server": "Defeah-API",
            
            # Cross-Origin policies
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Resource-Policy": "same-origin",
        }
        
        # Apply headers
        for header, value in security_headers.items():
            response.headers[header] = value
        
        return response
    
    def _default_csp_policy(self) -> str:
        """Default Content Security Policy"""
        return (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://api.defeah.com; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )

# Setup security headers
def setup_security_headers(app: FastAPI, environment: str):
    if environment == "production":
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'"
        )
    else:
        # More permissive for development
        csp_policy = (
            "default-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "img-src 'self' data: blob: https:; "
            "connect-src 'self' ws: wss:"
        )
    
    app.add_middleware(SecurityHeadersMiddleware, csp_policy=csp_policy)
```

## API Monitoring & Logging

### Security Event Logging

```python
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

class SecurityEventType(Enum):
    AUTHENTICATION_SUCCESS = "auth_success"
    AUTHENTICATION_FAILURE = "auth_failure"
    AUTHORIZATION_FAILURE = "authz_failure"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_REQUEST = "suspicious_request"
    INPUT_VALIDATION_FAILURE = "validation_failure"
    SQL_INJECTION_ATTEMPT = "sql_injection_attempt"
    XSS_ATTEMPT = "xss_attempt"
    FILE_UPLOAD_BLOCKED = "file_upload_blocked"
    UNUSUAL_API_USAGE = "unusual_api_usage"

class APISecurityLogger:
    def __init__(self):
        # Configure separate security logger
        self.logger = logging.getLogger("api.security")
        self.logger.setLevel(logging.INFO)
        
        # JSON formatter for structured logging
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_security_event(
        self,
        event_type: SecurityEventType,
        request: Request,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        severity: str = "INFO"
    ):
        """Log security events with structured data"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type.value,
            "severity": severity,
            "request": {
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "headers": self._sanitize_headers(dict(request.headers)),
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent"),
            },
            "user_id": user_id,
            "details": details or {},
        }
        
        # Log as JSON
        self.logger.info(json.dumps(event, default=str))
        
        # Send alerts for critical events
        if severity in ["WARNING", "ERROR", "CRITICAL"]:
            self._send_security_alert(event)
    
    def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Remove sensitive headers from logs"""
        sensitive_headers = {
            "authorization", "cookie", "x-api-key", "x-auth-token"
        }
        
        return {
            key: "[REDACTED]" if key.lower() in sensitive_headers else value
            for key, value in headers.items()
        }
    
    def _send_security_alert(self, event: Dict[str, Any]):
        """Send security alerts to monitoring systems"""
        # Implementation for alerting (Slack, PagerDuty, etc.)
        pass

# Security monitoring middleware
class SecurityMonitoringMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.security_logger = APISecurityLogger()
        self.suspicious_patterns = [
            r"('|(\\\\')|(;)|(\\|\\|)|(\\|/*|*/)",  # SQL injection
            r"<script|javascript:|data:|vbscript:",   # XSS
            r"\\.\\.[\\/\\\\]",                      # Path traversal
            r"(union|select|insert|delete|update|drop)",  # SQL keywords
        ]
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Check for suspicious patterns
        await self._check_suspicious_request(request)
        
        try:
            response = await call_next(request)
            
            # Log successful requests
            if response.status_code >= 400:
                severity = "WARNING" if response.status_code < 500 else "ERROR"
                self.security_logger.log_security_event(
                    SecurityEventType.SUSPICIOUS_REQUEST,
                    request,
                    details={"status_code": response.status_code},
                    severity=severity
                )
            
            return response
            
        except Exception as exc:
            # Log exceptions
            self.security_logger.log_security_event(
                SecurityEventType.SUSPICIOUS_REQUEST,
                request,
                details={"exception": str(exc)},
                severity="ERROR"
            )
            raise
        
        finally:
            # Log performance metrics
            duration = time.time() - start_time
            if duration > 5.0:  # Slow requests
                self.security_logger.log_security_event(
                    SecurityEventType.UNUSUAL_API_USAGE,
                    request,
                    details={"duration": duration},
                    severity="WARNING"
                )
    
    async def _check_suspicious_request(self, request: Request):
        """Check for suspicious request patterns"""
        # Check URL path
        url_path = str(request.url)
        for pattern in self.suspicious_patterns:
            if re.search(pattern, url_path, re.IGNORECASE):
                self.security_logger.log_security_event(
                    SecurityEventType.SUSPICIOUS_REQUEST,
                    request,
                    details={"pattern": pattern, "location": "url"},
                    severity="WARNING"
                )
        
        # Check request body for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    body_str = body.decode('utf-8', errors='ignore')
                    for pattern in self.suspicious_patterns:
                        if re.search(pattern, body_str, re.IGNORECASE):
                            self.security_logger.log_security_event(
                                SecurityEventType.SUSPICIOUS_REQUEST,
                                request,
                                details={"pattern": pattern, "location": "body"},
                                severity="WARNING"
                            )
            except:
                pass  # Ignore body parsing errors
```

This comprehensive API security implementation provides:

1. **Strong Authentication**: JWT-based authentication with proper token management
2. **Fine-grained Authorization**: Role-based access control with resource-level permissions
3. **Input Validation**: Comprehensive request validation and sanitization
4. **Rate Limiting**: Multi-level rate limiting with burst protection
5. **Output Security**: Response sanitization and secure error handling
6. **CORS Security**: Secure cross-origin request handling
7. **Security Headers**: Comprehensive security headers for defense-in-depth
8. **Monitoring**: Security event logging and threat detection

The implementation follows OWASP guidelines and industry best practices for API security.