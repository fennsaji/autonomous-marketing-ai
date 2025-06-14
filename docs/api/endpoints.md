# API Endpoints Reference

Complete reference for all Defeah Marketing Backend API endpoints.

## Authentication Endpoints

### POST /api/v1/auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "bio": "Home decor enthusiast",
  "timezone": "UTC"
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "bio": "Home decor enthusiast",
    "timezone": "UTC",
    "is_active": true,
    "is_verified": false,
    "instagram_connected": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "message": "User registered successfully",
  "status": "success"
}
```

**Validation Rules:**
- Email must be valid format
- Password minimum 8 characters
- Full name optional but recommended
- Timezone defaults to UTC

---

### POST /api/v1/auth/login

Authenticate user and return JWT token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 604800,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "instagram_connected": false
  }
}
```

---

### GET /api/v1/auth/me

Get current authenticated user information.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "bio": "Home decor enthusiast",
    "timezone": "UTC",
    "is_active": true,
    "is_verified": false,
    "instagram_connected": true,
    "instagram_username": "@homedecor_lover",
    "notification_preferences": {
      "email_analytics": true,
      "email_post_published": false,
      "push_engagement": true
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### POST /api/v1/auth/refresh

Refresh JWT access token.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 604800,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "instagram_connected": true
  }
}
```

---

### POST /api/v1/auth/logout

Logout user (client-side token invalidation).

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "message": "Successfully logged out",
  "status": "success"
}
```

## Instagram Integration Endpoints

### POST /api/v1/auth/instagram/connect

Connect Instagram Business account via OAuth.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "auth_code": "instagram_oauth_authorization_code"
}
```

**Response (200 OK):**
```json
{
  "message": "Instagram account connected successfully",
  "instagram_user_id": "17841400455970022",
  "username": "homedecor_lover"
}
```

---

### DELETE /api/v1/auth/instagram/disconnect

Disconnect Instagram account.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "message": "Instagram account disconnected successfully"
}
```

---

### GET /api/v1/instagram/profile

Get connected Instagram account profile information.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "data": {
    "instagram_user_id": "17841400455970022",
    "username": "homedecor_lover",
    "account_type": "BUSINESS",
    "media_count": 142,
    "connected": true
  }
}
```

---

### GET /api/v1/instagram/permissions

Check Instagram account permissions and eligibility.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "can_publish": true,
  "account_type": "business",
  "permissions": [
    "instagram_basic",
    "instagram_content_publish"
  ]
}
```

## Content Management Endpoints

### GET /api/v1/posts

List posts with filtering and pagination.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20, max: 100)
- `status` (string): Filter by status (`draft`, `scheduled`, `published`)
- `created_after` (date): Filter posts created after date
- `search` (string): Search in title and caption

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174000",
      "title": "Cozy Living Room Setup",
      "caption": "Transform your living space with these cozy decor ideas! 🏡✨",
      "hashtags": ["#homedecor", "#interiordesign", "#cozy"],
      "media_url": "https://storage.defeah.com/images/post-123.jpg",
      "status": "published",
      "scheduled_at": null,
      "published_at": "2024-01-15T14:30:00Z",
      "instagram_post_id": "17895695668004550",
      "analytics": {
        "likes": 245,
        "comments": 18,
        "shares": 12,
        "reach": 1850,
        "engagement_rate": 14.9
      },
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T14:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 47,
    "pages": 3
  }
}
```

---

### POST /api/v1/posts

Create a new post.

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "title": "Beautiful Kitchen Design",
  "caption": "Modern kitchen inspiration for your home renovation! 🍳✨",
  "hashtags": ["#kitchendesign", "#homedecor", "#renovation"],
  "media_url": "https://storage.defeah.com/images/kitchen-design.jpg",
  "status": "draft",
  "scheduled_at": "2024-01-16T15:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "789e1234-e89b-12d3-a456-426614174000",
    "title": "Beautiful Kitchen Design",
    "caption": "Modern kitchen inspiration for your home renovation! 🍳✨",
    "hashtags": ["#kitchendesign", "#homedecor", "#renovation"],
    "media_url": "https://storage.defeah.com/images/kitchen-design.jpg",
    "status": "draft",
    "scheduled_at": "2024-01-16T15:00:00Z",
    "published_at": null,
    "instagram_post_id": null,
    "created_at": "2024-01-15T11:30:00Z",
    "updated_at": "2024-01-15T11:30:00Z"
  },
  "message": "Post created successfully"
}
```

---

### GET /api/v1/posts/{id}

Get specific post details.

**Headers:** `Authorization: Bearer <token>`

**Path Parameters:**
- `id` (UUID): Post ID

**Response (200 OK):**
```json
{
  "data": {
    "id": "789e1234-e89b-12d3-a456-426614174000",
    "title": "Beautiful Kitchen Design",
    "caption": "Modern kitchen inspiration for your home renovation! 🍳✨",
    "hashtags": ["#kitchendesign", "#homedecor", "#renovation"],
    "media_url": "https://storage.defeah.com/images/kitchen-design.jpg",
    "status": "scheduled",
    "scheduled_at": "2024-01-16T15:00:00Z",
    "published_at": null,
    "instagram_post_id": null,
    "ai_generated": {
      "caption_generated": true,
      "hashtags_suggested": true,
      "generation_cost": 0.05
    },
    "campaign_id": "321e5678-e89b-12d3-a456-426614174000",
    "created_at": "2024-01-15T11:30:00Z",
    "updated_at": "2024-01-15T11:30:00Z"
  }
}
```

---

### PUT /api/v1/posts/{id}

Update existing post.

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "title": "Stunning Kitchen Renovation",
  "caption": "Updated caption with more details about the renovation process! 🏠✨",
  "hashtags": ["#kitchenrenovation", "#homedecor", "#interiordesign"],
  "scheduled_at": "2024-01-16T16:00:00Z"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "789e1234-e89b-12d3-a456-426614174000",
    "title": "Stunning Kitchen Renovation",
    "caption": "Updated caption with more details about the renovation process! 🏠✨",
    "hashtags": ["#kitchenrenovation", "#homedecor", "#interiordesign"],
    "media_url": "https://storage.defeah.com/images/kitchen-design.jpg",
    "status": "scheduled",
    "scheduled_at": "2024-01-16T16:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  },
  "message": "Post updated successfully"
}
```

---

### DELETE /api/v1/posts/{id}

Delete a post.

**Headers:** `Authorization: Bearer <token>`

**Response (204 No Content)**

---

### POST /api/v1/posts/{id}/publish

Manually publish a post to Instagram.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "data": {
    "id": "789e1234-e89b-12d3-a456-426614174000",
    "status": "published",
    "published_at": "2024-01-15T12:30:00Z",
    "instagram_post_id": "17895695668004550",
    "instagram_permalink": "https://www.instagram.com/p/ABC123DEF456/"
  },
  "message": "Post published successfully to Instagram"
}
```

## Campaign Management Endpoints

### GET /api/v1/campaigns

List campaigns with filtering.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page`, `limit` - Pagination
- `status` - Filter by status (`draft`, `active`, `paused`, `completed`)
- `created_after` - Filter by creation date

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "321e5678-e89b-12d3-a456-426614174000",
      "name": "Winter Home Decor Collection",
      "description": "Showcase cozy winter decor ideas",
      "status": "active",
      "theme": "winter_cozy",
      "post_count": 12,
      "published_count": 8,
      "budget": 150.00,
      "spent": 89.50,
      "start_date": "2024-01-01T00:00:00Z",
      "end_date": "2024-01-31T23:59:59Z",
      "performance": {
        "total_reach": 25000,
        "total_engagement": 1850,
        "avg_engagement_rate": 7.4,
        "roi": 245.8
      },
      "created_at": "2023-12-20T10:00:00Z",
      "updated_at": "2024-01-15T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 5,
    "pages": 1
  }
}
```

---

### POST /api/v1/campaigns

Create a new campaign.

**Request Body:**
```json
{
  "name": "Spring Home Refresh",
  "description": "Fresh spring decor ideas and inspiration",
  "theme": "spring_fresh",
  "budget": 200.00,
  "start_date": "2024-03-01T00:00:00Z",
  "end_date": "2024-03-31T23:59:59Z",
  "settings": {
    "auto_generate_content": true,
    "posting_frequency": "daily",
    "optimal_times": ["09:00", "15:00", "19:00"]
  }
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "654e9012-e89b-12d3-a456-426614174000",
    "name": "Spring Home Refresh",
    "description": "Fresh spring decor ideas and inspiration",
    "status": "draft",
    "theme": "spring_fresh",
    "budget": 200.00,
    "spent": 0.00,
    "start_date": "2024-03-01T00:00:00Z",
    "end_date": "2024-03-31T23:59:59Z",
    "settings": {
      "auto_generate_content": true,
      "posting_frequency": "daily",
      "optimal_times": ["09:00", "15:00", "19:00"]
    },
    "created_at": "2024-01-15T13:00:00Z",
    "updated_at": "2024-01-15T13:00:00Z"
  },
  "message": "Campaign created successfully"
}
```

## AI Content Generation Endpoints

### POST /api/v1/content/caption/generate

Generate AI-powered caption for posts.

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "prompt": "Cozy living room with neutral colors",
  "style": "engaging",
  "length": "medium",
  "include_hashtags": true,
  "brand_voice": "friendly_expert"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "caption": "Transform your living space into a cozy sanctuary with these neutral color palettes! 🏡 The perfect blend of comfort and style creates an inviting atmosphere that welcomes you home every day. ✨",
    "hashtags": ["#homedecor", "#interiordesign", "#cozyvibes", "#neutralpalette", "#livingroomdesign"],
    "word_count": 34,
    "character_count": 186,
    "generation_cost": 0.03,
    "brand_consistency_score": 92
  },
  "message": "Caption generated successfully"
}
```

---

### POST /api/v1/content/hashtags/suggest

Get AI-suggested hashtags for content.

**Request Body:**
```json
{
  "content": "Beautiful kitchen renovation with marble countertops",
  "category": "kitchen",
  "target_audience": "homeowners",
  "max_hashtags": 20
}
```

**Response (200 OK):**
```json
{
  "data": {
    "hashtags": [
      "#kitchenrenovation",
      "#marblecountertops", 
      "#kitchendesign",
      "#homedecor",
      "#renovation",
      "#interiordesign",
      "#kitchenremodel",
      "#modernkitchen",
      "#luxurykitchen",
      "#homeimprovement"
    ],
    "relevance_scores": [95, 90, 88, 85, 83, 80, 78, 75, 72, 70],
    "total_reach_estimate": 2850000,
    "competition_level": "medium",
    "generation_cost": 0.02
  }
}
```

---

### POST /api/v1/content/analyze

Analyze content performance and get optimization suggestions.

**Request Body:**
```json
{
  "post_id": "789e1234-e89b-12d3-a456-426614174000",
  "analysis_type": "comprehensive"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "performance_score": 87,
    "engagement_analysis": {
      "likes_score": 92,
      "comments_score": 78,
      "shares_score": 85,
      "saves_score": 90
    },
    "content_analysis": {
      "caption_effectiveness": 88,
      "hashtag_performance": 82,
      "visual_appeal": 94,
      "posting_time_optimization": 76
    },
    "recommendations": [
      {
        "type": "hashtag_optimization",
        "suggestion": "Consider adding trending hashtags like #homedecortrends",
        "impact": "medium",
        "priority": "high"
      },
      {
        "type": "posting_time",
        "suggestion": "Post 2 hours earlier for better engagement",
        "impact": "high",
        "priority": "medium"
      }
    ],
    "competitive_analysis": {
      "ranking": "top_25_percent",
      "similar_posts_avg_engagement": 156,
      "your_post_engagement": 198
    }
  }
}
```

## System Endpoints

### GET /health

System health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": 1642262400,
  "version": "1.0.0",
  "environment": "production",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "instagram_api": "healthy",
    "openai_api": "healthy"
  }
}
```

---

### GET /

Root API information endpoint.

**Response (200 OK):**
```json
{
  "message": "Defeah Marketing Backend",
  "version": "1.0.0",
  "environment": "production",
  "docs_url": "/docs",
  "api_version": "v1"
}
```

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "email": ["Invalid email format"],
      "password": ["Password must be at least 8 characters"]
    }
  },
  "status": "error"
}
```

### 401 Unauthorized
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required",
    "details": {
      "hint": "Include valid JWT token in Authorization header"
    }
  },
  "status": "error"
}
```

### 403 Forbidden
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions",
    "details": {
      "required_permission": "instagram:publish",
      "user_permissions": ["instagram:read"]
    }
  },
  "status": "error"
}
```

### 404 Not Found
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": {
      "resource_type": "post",
      "resource_id": "789e1234-e89b-12d3-a456-426614174000"
    }
  },
  "status": "error"
}
```

### 429 Too Many Requests
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 1000,
      "window": "1 hour",
      "retry_after": 3600
    }
  },
  "status": "error"
}
```

### 500 Internal Server Error
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Internal server error",
    "details": {
      "request_id": "550e8400-e29b-41d4-a716-446655440000",
      "support_email": "support@defeah.com"
    }
  },
  "status": "error"
}
```