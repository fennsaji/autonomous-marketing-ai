# Defeah Marketing API Documentation

## Base Information

**Base URL:** `https://api.defeah.com/api/v1`

**Authentication:** Bearer Token (JWT)

**Content-Type:** `application/json` (unless specified otherwise)

## Authentication

### Register User
```
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "full_name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z",
  "instagram_connected": false
}
```

**Error Response (400):**
```json
{
  "detail": "Email already registered",
  "error_code": "EMAIL_ALREADY_EXISTS"
}
```

### Login User
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded
```

**Request Body:**
```
username=user@example.com&password=securePassword123
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 604800,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "instagram_connected": false
  }
}
```

**Error Response (401):**
```json
{
  "detail": "Incorrect email or password",
  "error_code": "INVALID_CREDENTIALS"
}
```

### Connect Instagram Account
```
POST /auth/instagram/connect
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "auth_code": "instagram_oauth_code_here"
}
```

**Response (200):**
```json
{
  "message": "Instagram account connected successfully",
  "instagram_user_id": "17841400123456789",
  "username": "defeah_official"
}
```

**Error Response (400):**
```json
{
  "detail": "Invalid Instagram authorization code",
  "error_code": "INVALID_AUTH_CODE"
}
```

### Get Current User
```
GET /auth/me
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "instagram_connected": true,
  "instagram_username": "defeah_official",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Posts Management

### Get All Posts
```
GET /posts?skip=0&limit=20&status=published&campaign_id=123
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `skip` (integer, optional): Number of posts to skip (default: 0)
- `limit` (integer, optional): Number of posts to return (default: 20, max: 100)
- `status` (string, optional): Filter by status (`draft`, `scheduled`, `published`, `failed`)
- `campaign_id` (string, optional): Filter by campaign ID

**Response (200):**
```json
{
  "posts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "caption": "Transform your living space with our modern collection ✨",
      "hashtags": ["#DefeahStyle", "#HomeDecor", "#ModernLiving"],
      "media_urls": ["https://cdn.defeah.com/image1.jpg"],
      "post_type": "photo",
      "status": "published",
      "scheduled_time": null,
      "published_at": "2024-01-15T10:30:00Z",
      "instagram_post_id": "18123456789",
      "instagram_permalink": "https://www.instagram.com/p/ABC123/",
      "campaign": {
        "id": "campaign-123",
        "name": "Spring Collection 2024"
      },
      "analytics": {
        "likes_count": 145,
        "comments_count": 12,
        "shares_count": 8,
        "saves_count": 23,
        "reach": 1250,
        "impressions": 2100,
        "engagement_rate": 15.2
      },
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 156,
  "page": 1,
  "pages": 8,
  "has_next": true,
  "has_prev": false
}
```

### Create Post
```
POST /posts
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "caption": "Discover the perfect blend of comfort and style ✨",
  "hashtags": ["#DefeahStyle", "#HomeDecor", "#CozyVibes"],
  "media_urls": ["https://cdn.defeah.com/image1.jpg"],
  "post_type": "photo",
  "campaign_id": "550e8400-e29b-41d4-a716-446655440000",
  "scheduled_time": "2024-01-16T14:00:00Z"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "caption": "Discover the perfect blend of comfort and style ✨",
  "hashtags": ["#DefeahStyle", "#HomeDecor", "#CozyVibes"],
  "media_urls": ["https://cdn.defeah.com/image1.jpg"],
  "post_type": "photo",
  "status": "scheduled",
  "scheduled_time": "2024-01-16T14:00:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Response (422):**
```json
{
  "detail": "Validation error",
  "error_code": "VALIDATION_ERROR",
  "errors": [
    {
      "field": "caption",
      "message": "Caption cannot exceed 2200 characters"
    }
  ]
}
```

### Get Single Post
```
GET /posts/{post_id}
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "caption": "Transform your living space...",
  "hashtags": ["#DefeahStyle", "#HomeDecor"],
  "media_urls": ["https://cdn.defeah.com/image1.jpg"],
  "post_type": "photo",
  "status": "published",
  "analytics": {
    "likes_count": 145,
    "comments_count": 12,
    "engagement_rate": 15.2
  }
}
```

**Error Response (404):**
```json
{
  "detail": "Post not found",
  "error_code": "POST_NOT_FOUND"
}
```

### Update Post
```
PUT /posts/{post_id}
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "caption": "Updated caption with new messaging",
  "hashtags": ["#DefeahStyle", "#UpdatedHashtag"],
  "scheduled_time": "2024-01-17T15:00:00Z"
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "caption": "Updated caption with new messaging",
  "hashtags": ["#DefeahStyle", "#UpdatedHashtag"],
  "scheduled_time": "2024-01-17T15:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

### Delete Post
```
DELETE /posts/{post_id}
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "message": "Post deleted successfully"
}
```

### Publish Post Immediately
```
POST /posts/{post_id}/publish
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "message": "Post published successfully",
  "instagram_post_id": "18123456789",
  "published_at": "2024-01-15T10:30:00Z"
}
```

**Error Response (400):**
```json
{
  "detail": "Instagram account not connected",
  "error_code": "INSTAGRAM_NOT_CONNECTED"
}
```

## AI Content Generation

### Generate Caption
```
POST /content/caption/generate
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "product_description": "Modern minimalist coffee table with oak wood finish",
  "tone": "professional",
  "style": "engaging",
  "include_hashtags": true,
  "max_length": 1500,
  "target_audience": "young_professionals",
  "call_to_action": "shop_now"
}
```

**Response (200):**
```json
{
  "caption": "Elevate your workspace with our stunning oak coffee table ☕✨ This minimalist masterpiece brings warmth and functionality to any room. Perfect for morning coffee moments and evening relaxation. Transform your space today! 🏡 #DefeahStyle #ModernFurniture #HomeOffice",
  "word_count": 45,
  "character_count": 280,
  "hashtags_included": 3,
  "model_used": "gpt-4",
  "tokens_used": 156,
  "cost_cents": 12,
  "generation_time_ms": 1250
}
```

**Error Response (429):**
```json
{
  "detail": "AI generation rate limit exceeded",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 3600
}
```

### Generate Image
```
POST /content/image/generate
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "prompt": "Modern oak coffee table in bright minimalist living room",
  "style": "photorealistic",
  "quality": "hd",
  "size": "1024x1024",
  "lighting": "natural",
  "background": "clean_minimalist"
}
```

**Response (200):**
```json
{
  "image_url": "https://cdn.openai.com/image_123456.jpg",
  "prompt_used": "Modern oak coffee table in bright minimalist living room, photorealistic style, natural lighting",
  "model_used": "dall-e-3",
  "size": "1024x1024",
  "quality": "hd",
  "cost_cents": 8,
  "generation_time_ms": 15000,
  "expires_at": "2024-01-22T10:30:00Z"
}
```

**Error Response (400):**
```json
{
  "detail": "Invalid image generation parameters",
  "error_code": "INVALID_PARAMETERS",
  "errors": [
    {
      "field": "size",
      "message": "Size must be one of: 1024x1024, 1024x1792, 1792x1024"
    }
  ]
}
```

### Suggest Hashtags
```
POST /content/hashtags/suggest
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "content_description": "Modern coffee table styled in living room",
  "niche": "home_decor",
  "count": 15,
  "competition_level": "medium",
  "include_branded": true
}
```

**Response (200):**
```json
{
  "hashtags": [
    "#DefeahStyle",
    "#HomeDecor",
    "#ModernFurniture",
    "#CoffeeTable",
    "#MinimalistHome",
    "#InteriorDesign",
    "#LivingRoomDecor"
  ],
  "total_count": 15,
  "competition_analysis": {
    "low_competition": 5,
    "medium_competition": 8,
    "high_competition": 2
  },
  "estimated_reach": {
    "min": 5000,
    "max": 50000
  }
}
```

## Campaign Management

### Get All Campaigns
```
GET /campaigns?skip=0&limit=20&is_active=true
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "campaigns": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Spring Collection 2024",
      "description": "Showcase our new spring home decor collection",
      "start_date": "2024-03-01T00:00:00Z",
      "end_date": "2024-05-31T23:59:59Z",
      "posts_per_day": 2,
      "is_active": true,
      "content_themes": ["spring_colors", "outdoor_living", "fresh_decor"],
      "brand_voice": "professional",
      "target_hashtags": ["#SpringDecor", "#OutdoorLiving", "#FreshStyle"],
      "performance": {
        "total_posts": 45,
        "avg_engagement_rate": 12.5,
        "total_reach": 125000,
        "total_impressions": 280000
      },
      "created_at": "2024-02-15T10:30:00Z"
    }
  ],
  "total": 8,
  "page": 1,
  "pages": 1
}
```

### Create Campaign
```
POST /campaigns
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Summer Outdoor Collection",
  "description": "Promote outdoor furniture and summer decor",
  "start_date": "2024-06-01T00:00:00Z",
  "end_date": "2024-08-31T23:59:59Z",
  "posts_per_day": 1,
  "content_themes": ["outdoor_furniture", "summer_vibes", "patio_decor"],
  "brand_voice": "casual",
  "target_hashtags": ["#SummerDecor", "#OutdoorFurniture", "#PatioStyle"],
  "target_reach": 50000,
  "target_engagement_rate": 10.0
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Summer Outdoor Collection",
  "description": "Promote outdoor furniture and summer decor",
  "start_date": "2024-06-01T00:00:00Z",
  "end_date": "2024-08-31T23:59:59Z",
  "posts_per_day": 1,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Get Campaign Analytics
```
GET /campaigns/{campaign_id}/analytics?period=last_30_days
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "campaign_id": "550e8400-e29b-41d4-a716-446655440000",
  "period": "last_30_days",
  "summary": {
    "total_posts": 30,
    "total_reach": 75000,
    "total_impressions": 150000,
    "total_engagement": 18500,
    "avg_engagement_rate": 12.3,
    "cost_per_engagement": 0.08,
    "roi_percentage": 235.5
  },
  "daily_breakdown": [
    {
      "date": "2024-01-15",
      "posts": 1,
      "reach": 2500,
      "impressions": 5000,
      "engagement": 615,
      "engagement_rate": 12.3
    }
  ],
  "top_performing_posts": [
    {
      "id": "post-123",
      "caption": "Transform your space...",
      "engagement_rate": 18.5,
      "reach": 5000
    }
  ]
}
```

### Update Campaign
```
PUT /campaigns/{campaign_id}
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Updated Campaign Name",
  "posts_per_day": 3,
  "is_active": false
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Updated Campaign Name",
  "posts_per_day": 3,
  "is_active": false,
  "updated_at": "2024-01-15T11:00:00Z"
}
```

### Delete Campaign
```
DELETE /campaigns/{campaign_id}
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "message": "Campaign deleted successfully"
}
```

## Analytics

### Get Account Analytics
```
GET /analytics/overview?period=last_30_days&metrics=all
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `period` (string): `last_7_days`, `last_30_days`, `last_90_days`, `custom`
- `start_date` (string, optional): Start date for custom period (ISO format)
- `end_date` (string, optional): End date for custom period (ISO format)
- `metrics` (string): `all`, `engagement`, `reach`, `growth`

**Response (200):**
```json
{
  "period": "last_30_days",
  "account_metrics": {
    "follower_count": 15420,
    "follower_growth": 324,
    "follower_growth_rate": 2.1,
    "total_posts": 45,
    "avg_posts_per_day": 1.5
  },
  "content_metrics": {
    "total_reach": 125000,
    "total_impressions": 280000,
    "total_engagement": 35000,
    "avg_engagement_rate": 12.5,
    "total_saves": 4500,
    "total_shares": 1200,
    "total_comments": 890,
    "total_likes": 28410
  },
  "top_content": {
    "most_engaging_post": {
      "id": "post-123",
      "engagement_rate": 25.3,
      "caption": "Transform your living space..."
    },
    "most_reached_post": {
      "id": "post-456",
      "reach": 8500,
      "caption": "Discover our latest collection..."
    }
  },
  "growth_trends": {
    "engagement_trend": "increasing",
    "reach_trend": "stable",
    "follower_trend": "increasing"
  }
}
```

### Get Post Performance
```
GET /analytics/posts/{post_id}/performance
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "post_id": "550e8400-e29b-41d4-a716-446655440000",
  "published_at": "2024-01-15T10:30:00Z",
  "performance_data": {
    "impressions": 5000,
    "reach": 4200,
    "likes": 340,
    "comments": 28,
    "shares": 15,
    "saves": 67,
    "engagement_rate": 14.3,
    "save_rate": 1.34,
    "share_rate": 0.3
  },
  "audience_insights": {
    "top_countries": ["US", "CA", "UK"],
    "age_demographics": {
      "18-24": 15,
      "25-34": 45,
      "35-44": 25,
      "45-54": 15
    },
    "gender_split": {
      "female": 68,
      "male": 32
    }
  },
  "time_analysis": {
    "peak_engagement_hour": 19,
    "engagement_by_hour": [
      {"hour": 9, "engagement": 45},
      {"hour": 12, "engagement": 78},
      {"hour": 19, "engagement": 156}
    ]
  }
}
```

## User Management

### Update Profile
```
PUT /users/profile
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "full_name": "John Doe Updated",
  "bio": "Home decor enthusiast and content creator",
  "timezone": "America/New_York",
  "notification_preferences": {
    "email_analytics": true,
    "email_post_published": false,
    "push_engagement": true
  }
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe Updated",
  "bio": "Home decor enthusiast and content creator",
  "timezone": "America/New_York",
  "notification_preferences": {
    "email_analytics": true,
    "email_post_published": false,
    "push_engagement": true
  },
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Get User Statistics
```
GET /users/statistics
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "account_age_days": 145,
  "total_posts_created": 234,
  "total_posts_published": 189,
  "total_ai_generations": {
    "captions": 145,
    "images": 67,
    "hashtags": 89
  },
  "spending": {
    "total_ai_cost_cents": 2450,
    "monthly_cost_cents": 380
  },
  "performance": {
    "avg_engagement_rate": 12.8,
    "best_engagement_rate": 28.5,
    "total_reach": 450000,
    "total_followers_gained": 1250
  }
}
```

## File Upload

### Upload Media Files
```
POST /media/upload
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
- `file`: Binary file data
- `type`: "image" | "video"
- `purpose`: "post" | "profile"

**Response (201):**
```json
{
  "file_id": "file_123456",
  "url": "https://cdn.defeah.com/uploads/file_123456.jpg",
  "type": "image",
  "size_bytes": 2048576,
  "dimensions": {
    "width": 1080,
    "height": 1080
  },
  "expires_at": "2024-01-22T10:30:00Z"
}
```

**Error Response (413):**
```json
{
  "detail": "File size exceeds maximum limit of 10MB",
  "error_code": "FILE_TOO_LARGE"
}
```

## Health Check

### System Health
```
GET /health
```

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "instagram_api": "healthy",
    "openai_api": "healthy"
  }
}
```

## Common Error Responses

### Rate Limit Exceeded (429)
```json
{
  "detail": "Rate limit exceeded. Try again in 3600 seconds.",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 3600,
  "rate_limit": {
    "limit": 1000,
    "remaining": 0,
    "reset": 1642276800
  }
}
```

### Unauthorized (401)
```json
{
  "detail": "Invalid or expired token",
  "error_code": "INVALID_TOKEN"
}
```

### Forbidden (403)
```json
{
  "detail": "Insufficient permissions",
  "error_code": "INSUFFICIENT_PERMISSIONS"
}
```

### Validation Error (422)
```json
{
  "detail": "Validation error",
  "error_code": "VALIDATION_ERROR",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    },
    {
      "field": "password",
      "message": "Password must be at least 8 characters"
    }
  ]
}
```

### Server Error (500)
```json
{
  "detail": "Internal server error",
  "error_code": "INTERNAL_ERROR",
  "request_id": "req_123456789"
}
```

## Rate Limiting

All endpoints have the following rate limit headers in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642276800
```

**Limits:**
- General API calls: 1000 requests/hour
- Content generation: 100 requests/hour
- Post publishing: 50 posts/day
- File uploads: 200 uploads/hour
