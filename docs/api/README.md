# API Documentation

Comprehensive API documentation for the Defeah Marketing Backend REST API.

## 📁 Documentation Structure

- **[Endpoints](./endpoints.md)** - Complete API endpoint reference
- **[Authentication](./authentication.md)** - Authentication and authorization guide
- **[Examples](./examples.md)** - Request/response examples and code samples
- **[Errors](./errors.md)** - Error codes, handling, and troubleshooting
- **[Rate Limiting](./rate-limiting.md)** - API rate limiting policies and headers
- **[Webhooks](./webhooks.md)** - Webhook endpoints and event handling

## 🚀 Quick Start

### Base URL
```
Production: https://api.defeah.com
Development: http://localhost:8080
```

### API Version
All API endpoints are versioned and prefixed with `/api/v1/`

### Authentication
The API uses JWT Bearer token authentication:
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     https://api.defeah.com/api/v1/users/me
```

### Content Type
All requests and responses use JSON:
```bash
curl -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -X POST \
     -d '{"email": "user@example.com"}' \
     https://api.defeah.com/api/v1/users
```

## 📋 API Overview

### Core Endpoints

#### Authentication
```
POST   /api/v1/auth/register      # User registration
POST   /api/v1/auth/login         # User login
POST   /api/v1/auth/refresh       # Token refresh
POST   /api/v1/auth/logout        # User logout
GET    /api/v1/auth/me            # Current user profile
```

#### User Management
```
GET    /api/v1/users/me           # Get current user
PUT    /api/v1/users/me           # Update current user
DELETE /api/v1/users/me           # Delete current user
```

#### Instagram Integration
```
POST   /api/v1/auth/instagram/connect     # Connect Instagram account
DELETE /api/v1/auth/instagram/disconnect  # Disconnect Instagram account
GET    /api/v1/instagram/profile          # Get Instagram profile
GET    /api/v1/instagram/permissions      # Check account permissions
```

#### Content Management
```
GET    /api/v1/posts               # List posts
POST   /api/v1/posts               # Create post
GET    /api/v1/posts/{id}          # Get post details
PUT    /api/v1/posts/{id}          # Update post
DELETE /api/v1/posts/{id}          # Delete post
POST   /api/v1/posts/{id}/publish  # Publish post to Instagram
```

#### Campaign Management
```
GET    /api/v1/campaigns           # List campaigns
POST   /api/v1/campaigns           # Create campaign
GET    /api/v1/campaigns/{id}      # Get campaign details
PUT    /api/v1/campaigns/{id}      # Update campaign
DELETE /api/v1/campaigns/{id}      # Delete campaign
```

#### AI Content Generation
```
POST   /api/v1/content/caption/generate    # Generate AI caption
POST   /api/v1/content/image/generate      # Generate AI image
POST   /api/v1/content/hashtags/suggest    # Suggest hashtags
POST   /api/v1/content/analyze             # Analyze content performance
```

### System Endpoints
```
GET    /health                     # System health check
GET    /docs                       # Interactive API documentation
GET    /openapi.json               # OpenAPI specification
```

## 🔧 Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "message": "User created successfully",
  "status": "success"
}
```

### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  },
  "status": "error"
}
```

### List Response
```json
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Beautiful Living Room"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  },
  "status": "success"
}
```

## 🔒 Authentication

### JWT Token Structure
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1642262400,
  "iat": 1642175000
}
```

### Token Usage
Include the JWT token in the Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Refresh
Refresh tokens before expiration:
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     https://api.defeah.com/api/v1/auth/refresh
```

## 📊 Rate Limiting

### Default Limits
- **General API**: 1000 requests per hour per user
- **Authentication**: 10 requests per minute per IP
- **AI Generation**: 100 requests per day per user
- **Instagram Publishing**: 50 requests per day per user

### Rate Limit Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642262400
X-RateLimit-RetryAfter: 3600
```

## 🎯 Status Codes

### Success Codes
- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content returned

### Client Error Codes
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict
- `422 Unprocessable Entity` - Validation error
- `429 Too Many Requests` - Rate limit exceeded

### Server Error Codes
- `500 Internal Server Error` - Server error
- `502 Bad Gateway` - Upstream service error
- `503 Service Unavailable` - Service temporarily unavailable

## 🔍 Filtering and Pagination

### Query Parameters
```bash
# Pagination
GET /api/v1/posts?page=1&limit=20

# Filtering
GET /api/v1/posts?status=published&created_after=2024-01-01

# Sorting
GET /api/v1/posts?sort=-created_at&sort=title

# Search
GET /api/v1/posts?search=home+decor
```

### Supported Operators
- `eq` - Equal to (default)
- `ne` - Not equal to
- `gt` - Greater than
- `gte` - Greater than or equal to
- `lt` - Less than
- `lte` - Less than or equal to
- `in` - In list
- `like` - Pattern matching

Example:
```bash
GET /api/v1/posts?created_at__gte=2024-01-01&status__in=published,scheduled
```

## 🌐 Internationalization

### Supported Languages
- `en` - English (default)
- `es` - Spanish
- `fr` - French

### Language Header
```
Accept-Language: en-US,en;q=0.9,es;q=0.8
```

## 📱 SDK and Libraries

### Official SDKs
- **Python**: `pip install defeah-marketing-sdk`
- **JavaScript**: `npm install @defeah/marketing-sdk`
- **PHP**: `composer require defeah/marketing-sdk`

### Community Libraries
- **Ruby**: `gem install defeah_marketing`
- **Go**: `go get github.com/defeah/go-marketing-sdk`

## 🧪 Testing

### Sandbox Environment
```
Base URL: https://sandbox-api.defeah.com
```

### Test Credentials
```json
{
  "email": "test@defeah.com",
  "password": "testpassword123"
}
```

### Postman Collection
Download our Postman collection for easy API testing:
[Defeah Marketing API.postman_collection.json](./postman/collection.json)

## 📈 Monitoring and Analytics

### Request Tracking
All API requests include a unique request ID:
```
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

### Performance Metrics
- Average response time: <200ms
- 99th percentile: <500ms
- Uptime: 99.9%

## 🔄 Versioning

### Current Version
- **v1** - Current stable version

### Version Support
- **v1**: Supported until 2025-12-31
- **Deprecation**: 6 months notice before deprecation

### Breaking Changes
Breaking changes will only be introduced in new major versions with proper migration guides.

## 📞 Support

### Developer Support
- **Documentation**: [docs.defeah.com](https://docs.defeah.com)
- **GitHub Issues**: [github.com/defeah/marketing-api/issues](https://github.com/defeah/marketing-api/issues)
- **Stack Overflow**: Tag questions with `defeah-marketing-api`

### Status Page
Monitor API status at: [status.defeah.com](https://status.defeah.com)

## 🔗 Related Resources

- [OpenAPI Specification](./openapi.json)
- [Interactive Documentation](http://localhost:8080/docs)
- [Authentication Guide](./authentication.md)
- [Rate Limiting Guide](./rate-limiting.md)
- [Error Handling Guide](./errors.md)
- [Code Examples](./examples.md)