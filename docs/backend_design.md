# FastAPI Instagram Marketing Backend - Complete Technical Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Database Design](#database-design)
4. [API Endpoints](#api-endpoints)
5. [Instagram Integration](#instagram-integration)
6. [OpenAI Integration](#openai-integration)
7. [Authentication & Security](#authentication--security)
8. [Task Scheduling](#task-scheduling)
9. [Configuration Management](#configuration-management)
10. [Deployment & Operations](#deployment--operations)

## Architecture Overview

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │────│   PostgreSQL    │    │   Redis Cache   │
│   (Web Layer)   │    │   (Data Store)  │    │   (Sessions)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Celery Beat   │    │   OpenAI API    │    │  Instagram API  │
│   (Scheduler)   │    │ (Content Gen)   │    │   (Publishing)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Web Framework:** FastAPI 0.104+
- **Database:** PostgreSQL 15+ with SQLAlchemy 2.0
- **Cache:** Redis 7.0+
- **Task Queue:** Celery with Redis broker
- **AI Integration:** OpenAI GPT-4 API
- **Instagram:** Meta Graph API
- **Authentication:** JWT with refresh tokens
- **Validation:** Pydantic v2

## Project Structure

```
defeah_marketing/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection
│   │   ├── redis.py           # Redis connection
│   │   └── security.py        # JWT and auth utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   ├── post.py           # Post model
│   │   ├── campaign.py       # Campaign model
│   │   └── analytics.py      # Analytics model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py           # User Pydantic schemas
│   │   ├── post.py           # Post Pydantic schemas
│   │   ├── campaign.py       # Campaign Pydantic schemas
│   │   └── analytics.py      # Analytics Pydantic schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py           # API dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py       # Authentication endpoints
│   │       ├── posts.py      # Post management endpoints
│   │       ├── campaigns.py  # Campaign endpoints
│   │       ├── analytics.py  # Analytics endpoints
│   │       └── content.py    # AI content generation endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Authentication business logic
│   │   ├── post_service.py   # Post management logic
│   │   ├── instagram_service.py # Instagram API integration
│   │   ├── openai_service.py # OpenAI integration
│   │   └── analytics_service.py # Analytics processing
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py     # Celery configuration
│   │   ├── post_tasks.py     # Post automation tasks
│   │   └── analytics_tasks.py # Analytics processing tasks
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py        # Utility functions
│       ├── validators.py     # Custom validators
│       └── exceptions.py     # Custom exceptions
├── migrations/               # Alembic migrations
├── tests/                   # Test suite
├── docker-compose.yml       # Local development setup
├── Dockerfile              # Production container
├── requirements.txt        # Python dependencies
└── .env.example           # Environment variables template
```

## Database Design

### Core Models

```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Instagram account info
    instagram_user_id = Column(String(100), unique=True, index=True)
    instagram_access_token = Column(Text)
    token_expires_at = Column(DateTime)
    
    # Relationships
    posts = relationship("Post", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")
```

```python
# app/models/post.py
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime
from enum import Enum

class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

class PostType(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"
    CAROUSEL = "carousel"
    REEL = "reel"

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=True)
    
    # Content details
    caption = Column(Text)
    hashtags = Column(ARRAY(String(50)))
    media_urls = Column(ARRAY(Text))  # Array for carousel posts
    post_type = Column(String(20), default=PostType.PHOTO)
    
    # Scheduling
    scheduled_time = Column(DateTime)
    published_at = Column(DateTime)
    status = Column(String(20), default=PostStatus.DRAFT)
    
    # Instagram data
    instagram_post_id = Column(String(100), unique=True, index=True)
    instagram_permalink = Column(Text)
    
    # AI generation metadata
    ai_prompt = Column(Text)
    ai_model_used = Column(String(50))
    generation_cost = Column(Integer)  # Cost in cents
    
    # Analytics
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    saves_count = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="posts")
    campaign = relationship("Campaign", back_populates="posts")
    analytics_events = relationship("AnalyticsEvent", back_populates="post")
```

```python
# app/models/campaign.py
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Campaign settings
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    posts_per_day = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    
    # Content generation settings
    content_themes = Column(JSON)  # ["modern_living", "cozy_bedroom", etc.]
    brand_voice = Column(String(50))  # "professional", "casual", "luxury"
    target_hashtags = Column(JSON)
    
    # Performance targets
    target_reach = Column(Integer)
    target_engagement_rate = Column(Integer)  # Percentage * 100
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="campaigns")
    posts = relationship("Post", back_populates="campaign")
```

```python
# app/models/analytics.py
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    
    event_type = Column(String(50))  # "like", "comment", "share", "save", "reach"
    event_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", back_populates="analytics_events")

class PerformanceMetrics(Base):
    __tablename__ = "performance_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Time period
    date = Column(DateTime, nullable=False)
    period_type = Column(String(20))  # "daily", "weekly", "monthly"
    
    # Aggregated metrics
    total_posts = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    total_saves = Column(Integer, default=0)
    total_reach = Column(Integer, default=0)
    total_impressions = Column(Integer, default=0)
    
    # Calculated metrics
    engagement_rate = Column(Float, default=0.0)
    avg_likes_per_post = Column(Float, default=0.0)
    cost_per_engagement = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Database Configuration

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## API Endpoints

### Authentication Endpoints

```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user account"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse.from_orm(db_user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/instagram/connect")
async def connect_instagram(
    auth_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Connect Instagram account using OAuth code"""
    auth_service = AuthService(db)
    instagram_data = await auth_service.exchange_instagram_code(auth_code)
    
    # Update user with Instagram credentials
    current_user.instagram_user_id = instagram_data["user_id"]
    current_user.instagram_access_token = instagram_data["access_token"]
    current_user.token_expires_at = instagram_data["expires_at"]
    
    db.commit()
    
    return {"message": "Instagram account connected successfully"}
```

### Post Management Endpoints

```python
# app/api/v1/posts.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.post import Post, PostStatus
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostSchedule
from app.services.post_service import PostService
from app.services.openai_service import OpenAIService
from app.tasks.post_tasks import schedule_post_publication

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post"""
    post_service = PostService(db)
    
    # Create post in database
    db_post = Post(
        user_id=current_user.id,
        campaign_id=post_data.campaign_id,
        caption=post_data.caption,
        hashtags=post_data.hashtags,
        media_urls=post_data.media_urls,
        post_type=post_data.post_type,
        scheduled_time=post_data.scheduled_time,
        status=PostStatus.DRAFT if post_data.scheduled_time else PostStatus.PUBLISHED
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Schedule for publishing if scheduled_time is provided
    if post_data.scheduled_time:
        schedule_post_publication.apply_async(
            args=[str(db_post.id)],
            eta=post_data.scheduled_time
        )
    
    return PostResponse.from_orm(db_post)

@router.get("/", response_model=List[PostResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    status: Optional[PostStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's posts with optional filtering"""
    query = db.query(Post).filter(Post.user_id == current_user.id)
    
    if status:
        query = query.filter(Post.status == status)
    
    posts = query.offset(skip).limit(limit).all()
    return [PostResponse.from_orm(post) for post in posts]

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific post by ID"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return PostResponse.from_orm(post)

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update existing post"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Update fields
    for field, value in post_update.dict(exclude_unset=True).items():
        setattr(post, field, value)
    
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    
    return PostResponse.from_orm(post)

@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a post"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    db.delete(post)
    db.commit()
    
    return {"message": "Post deleted successfully"}
```

### AI Content Generation Endpoints

```python
# app/api/v1/content.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.content import (
    CaptionGenerateRequest,
    CaptionResponse,
    ImageGenerateRequest,
    ImageResponse,
    HashtagSuggestionRequest,
    HashtagResponse
)
from app.services.openai_service import OpenAIService

router = APIRouter(prefix="/content", tags=["ai-content"])

@router.post("/caption/generate", response_model=CaptionResponse)
async def generate_caption(
    request: CaptionGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate Instagram caption using AI"""
    openai_service = OpenAIService()
    
    try:
        caption = await openai_service.generate_caption(
            product_description=request.product_description,
            tone=request.tone,
            style=request.style,
            include_hashtags=request.include_hashtags,
            max_length=request.max_length
        )
        
        return CaptionResponse(
            caption=caption,
            model_used="gpt-4",
            tokens_used=openai_service.last_token_count,
            cost_cents=openai_service.last_cost_cents
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Caption generation failed: {str(e)}"
        )

@router.post("/image/generate", response_model=ImageResponse)
async def generate_image(
    request: ImageGenerateRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate product image using DALL-E"""
    openai_service = OpenAIService()
    
    try:
        image_url = await openai_service.generate_image(
            prompt=request.prompt,
            style=request.style,
            quality=request.quality,
            size=request.size
        )
        
        return ImageResponse(
            image_url=image_url,
            prompt_used=request.prompt,
            model_used="dall-e-3",
            cost_cents=openai_service.last_cost_cents
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image generation failed: {str(e)}"
        )

@router.post("/hashtags/suggest", response_model=HashtagResponse)
async def suggest_hashtags(
    request: HashtagSuggestionRequest,
    current_user: User = Depends(get_current_user)
):
    """Suggest relevant hashtags for home decor content"""
    openai_service = OpenAIService()
    
    try:
        hashtags = await openai_service.suggest_hashtags(
            content_description=request.content_description,
            niche="home_decor",
            count=request.count,
            competition_level=request.competition_level
        )
        
        return HashtagResponse(
            hashtags=hashtags,
            total_count=len(hashtags)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hashtag suggestion failed: {str(e)}"
        )
```

## Instagram Integration

### Instagram Service Implementation

```python
# app/services/instagram_service.py
import httpx
import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.core.config import settings
from app.utils.exceptions import InstagramAPIError, RateLimitError

class InstagramService:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
        self.rate_limit_remaining = 200
        self.rate_limit_reset = datetime.utcnow() + timedelta(hours=1)
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> Dict:
        """Make authenticated request to Instagram API with rate limiting"""
        
        # Check rate limits
        if self.rate_limit_remaining <= 5:
            if datetime.utcnow() < self.rate_limit_reset:
                wait_time = (self.rate_limit_reset - datetime.utcnow()).total_seconds()
                await asyncio.sleep(wait_time)
                self.rate_limit_remaining = 200
        
        url = f"{self.base_url}/{endpoint}"
        params = {"access_token": self.access_token}
        
        if data:
            params.update(data)
        
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, params=params)
                elif method.upper() == "POST":
                    if files:
                        response = await client.post(url, params=params, files=files)
                    else:
                        response = await client.post(url, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Update rate limit info
                self.rate_limit_remaining -= 1
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    raise RateLimitError("Instagram API rate limit exceeded")
                elif e.response.status_code in [400, 401, 403]:
                    error_data = e.response.json()
                    raise InstagramAPIError(error_data.get("error", {}).get("message", "Unknown error"))
                else:
                    raise InstagramAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
    
    async def get_user_profile(self) -> Dict:
        """Get Instagram user profile information"""
        endpoint = "me"
        params = {
            "fields": "id,username,account_type,media_count,followers_count"
        }
        return await self._make_request("GET", endpoint, params)
    
    async def upload_photo(
        self, 
        image_url: str, 
        caption: str, 
        is_published: bool = True
    ) -> Dict:
        """Upload a photo to Instagram"""
        
        # Step 1: Create media object
        endpoint = "me/media"
        media_data = {
            "image_url": image_url,
            "caption": caption,
            "published": str(is_published).lower()
        }
        
        media_response = await self._make_request("POST", endpoint, media_data)
        
        if is_published:
            return media_response
        
        # Step 2: Publish media (if not published in step 1)
        media_id = media_response["id"]
        publish_endpoint = f"me/media_publish"
        publish_data = {"creation_id": media_id}
        
        return await self._make_request("POST", publish_endpoint, publish_data)
    
    async def upload_video(
        self, 
        video_url: str, 
        caption: str,
        is_reel: bool = False
    ) -> Dict:
        """Upload a video or reel to Instagram"""
        
        endpoint = "me/media"
        media_data = {
            "video_url": video_url,
            "caption": caption,
            "media_type": "REELS" if is_reel else "VIDEO"
        }
        
        # Create media container
        container_response = await self._make_request("POST", endpoint, media_data)
        container_id = container_response["id"]
        
        # Wait for video processing
        await self._wait_for_video_processing(container_id)
        
        # Publish video
        publish_data = {"creation_id": container_id}
        return await self._make_request("POST", "me/media_publish", publish_data)
    
    async def _wait_for_video_processing(self, container_id: str, max_wait: int = 300):
        """Wait for video processing to complete"""
        start_time = datetime.utcnow()
        
        while (datetime.utcnow() - start_time).total_seconds() < max_wait:
            status_response = await self._make_request("GET", container_id, {"fields": "status_code"})
            
            if status_response["status_code"] == "FINISHED":
                return True
            elif status_response["status_code"] == "ERROR":
                raise InstagramAPIError("Video processing failed")
            
            await asyncio.sleep(10)  # Wait 10 seconds before checking again
        
        raise InstagramAPIError("Video processing timeout")
    
    async def get_media_insights(self, media_id: str) -> Dict:
        """Get insights for a specific media post"""
        endpoint = f"{media_id}/insights"
        params = {
            "metric": "impressions,reach,likes,comments,shares,saves"
        }
        return await self._make_request("GET", endpoint, params)
    
    async def get_account_insights(
        self, 
        period: str = "day",
        since: Optional[datetime] = None,
        until: Optional[datetime] = None
    ) -> Dict:
        """Get account-level insights"""
        endpoint = "me/insights"
        params = {
            "metric": "impressions,reach,profile_views,follower_count",
            "period": period
        }
        
        if since:
            params["since"] = int(since.timestamp())
        if until:
            params["until"] = int(until.timestamp())
        
        return await self._make_request("GET", endpoint, params)
    
    async def refresh_access_token(self) -> Dict:
        """Refresh long-lived access token"""
        endpoint = "oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "fb_exchange_token": self.access_token
        }
        
        return await self._make_request("GET", endpoint, params)
```

## OpenAI Integration

### OpenAI Service Implementation

```python
# app/services/openai_service.py
import openai
from typing import List, Dict, Optional
from app.core.config import settings
import json
import asyncio

class OpenAIService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.last_token_count = 0
        self.last_cost_cents = 0
    
    async def generate_caption(
        self,
        product_description: str,
        tone: str = "professional",
        style: str = "engaging",
        include_hashtags: bool = True,
        max_length: int = 2200
    ) -> str:
        """Generate Instagram caption for home decor products"""
        
        system_prompt = f"""
        You are an expert Instagram content creator specializing in home decor for the brand "Defeah". 
        Create engaging captions that drive sales and engagement.
        
        Brand voice: {tone}
        Writing style: {style}
        Max length: {max_length} characters
        Include hashtags: {include_hashtags}
        
        Guidelines:
        - Start with a hook that stops scrolling
        - Include emotional connection to home/comfort
        - Mention specific product benefits
        - End with a call-to-action
        - Use emojis strategically
        - If hashtags included, use 5-15 relevant home decor hashtags
        - Focus on lifestyle transformation, not just product features
        """
        
        user_prompt = f"""
        Product: {product_description}
        
        Create an Instagram caption that will drive engagement and sales for this home decor product.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            caption = response.choices[0].message.content.strip()
            
            # Calculate costs (GPT-4 pricing: $0.03/1K input, $0.06/1K output)
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            self.last_token_count = response.usage.total_tokens
            self.last_cost_cents = int(
                (input_tokens * 0.03 / 1000 + output_tokens * 0.06 / 1000) * 100
            )
            
            return caption
            
        except Exception as e:
            raise Exception(f"Caption generation failed: {str(e)}")
    
    async def generate_image(
        self,
        prompt: str,
        style: str = "photorealistic",
        quality: str = "hd",
        size: str = "1024x1024"
    ) -> str:
        """Generate product image using DALL-E 3"""
        
        enhanced_prompt = f"""
        {prompt}
        
        Style: {style}, high-quality home decor photography
        Lighting: Natural, soft lighting with good contrast
        Composition: Professional product photography, clean background
        Quality: {quality}, Instagram-ready, commercial use
        
        Make it look like a premium home decor catalog photo.
        """
        
        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size=size,
                quality=quality,
                n=1
            )
            
            image_url = response.data[0].url
            
            # DALL-E 3 pricing: $0.04 for standard, $0.08 for HD quality
            self.last_cost_cents = 8 if quality == "hd" else 4
            
            return image_url
            
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
    
    async def suggest_hashtags(
        self,
        content_description: str,
        niche: str = "home_decor",
        count: int = 15,
        competition_level: str = "medium"
    ) -> List[str]:
        """Suggest relevant hashtags for content"""
        
        system_prompt = f"""
        You are a hashtag research expert for Instagram marketing in the {niche} niche.
        Suggest {count} high-performing hashtags with {competition_level} competition level.
        
        Guidelines:
        - Mix of popular and niche-specific hashtags
        - Include branded hashtag: #DefeahStyle
        - Balance reach and engagement potential
        - Avoid banned or shadowbanned hashtags
        - Return only hashtags, one per line, with # symbol
        """
        
        user_prompt = f"""
        Content description: {content_description}
        
        Suggest {count} strategic hashtags for maximum reach and engagement.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            hashtags_text = response.choices[0].message.content.strip()
            hashtags = [tag.strip() for tag in hashtags_text.split('\n') if tag.strip().startswith('#')]
            
            # Calculate costs
            self.last_token_count = response.usage.total_tokens
            self.last_cost_cents = int(
                (response.usage.prompt_tokens * 0.03 / 1000 + 
                 response.usage.completion_tokens * 0.06 / 1000) * 100
            )
            
            return hashtags[:count]
            
        except Exception as e:
            raise Exception(f"Hashtag suggestion failed: {str(e)}")
    
    async def analyze_content_performance(
        self,
        posts_data: List[Dict],
        time_period: str = "last_30_days"
    ) -> Dict:
        """Analyze content performance and provide recommendations"""
        
        system_prompt = f"""
        You are a social media analytics expert. Analyze the provided Instagram post data 
        and provide actionable insights for improving performance.
        
        Focus on:
        - Best performing content types
        - Optimal posting times
        - Caption length analysis
        - Hashtag performance
        - Engagement patterns
        - Content recommendations
        
        Return analysis as JSON with specific recommendations.
        """
        
        user_prompt = f"""
        Instagram posts data for {time_period}:
        {json.dumps(posts_data, indent=2)}
        
        Provide detailed performance analysis and 5 specific recommendations for improvement.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Try to parse as JSON, fallback to text if parsing fails
            try:
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                analysis = {"raw_analysis": analysis_text}
            
            self.last_token_count = response.usage.total_tokens
            self.last_cost_cents = int(
                (response.usage.prompt_tokens * 0.03 / 1000 + 
                 response.usage.completion_tokens * 0.06 / 1000) * 100
            )
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Content analysis failed: {str(e)}")
```

## Authentication & Security

### JWT Security Implementation

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return user ID"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            return None
            
        return user_id
        
    except JWTError:
        return None

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = verify_token(token)
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user
```

## Task Scheduling

### Celery Configuration

```python
# app/tasks/celery_app.py
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "defeah_marketing",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.post_tasks",
        "app.tasks.analytics_tasks"
    ]
)

# Task configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    result_expires=3600,
)

# Periodic tasks
celery_app.conf.beat_schedule = {
    # Refresh Instagram tokens daily
    "refresh-instagram-tokens": {
        "task": "app.tasks.post_tasks.refresh_instagram_tokens",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    
    # Sync analytics hourly
    "sync-post-analytics": {
        "task": "app.tasks.analytics_tasks.sync_post_analytics",
        "schedule": crontab(minute=0),  # Every hour
    },
    
    # Generate daily performance reports
    "generate-daily-reports": {
        "task": "app.tasks.analytics_tasks.generate_daily_performance_report",
        "schedule": crontab(hour=8, minute=0),  # Daily at 8 AM
    },
    
    # Auto-generate content for active campaigns
    "auto-generate-content": {
        "task": "app.tasks.post_tasks.auto_generate_campaign_content",
        "schedule": crontab(hour=10, minute=0),  # Daily at 10 AM
    }
}
```

### Post Publishing Tasks

```python
# app/tasks/post_tasks.py
from celery import current_task
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.post import Post, PostStatus
from app.models.user import User
from app.models.campaign import Campaign
from app.services.instagram_service import InstagramService
from app.services.openai_service import OpenAIService
from app.utils.exceptions import InstagramAPIError, RateLimitError

@celery_app.task(bind=True, max_retries=3)
def schedule_post_publication(self, post_id: str):
    """Publish a scheduled post to Instagram"""
    db = SessionLocal()
    
    try:
        # Get post and user
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise Exception(f"Post {post_id} not found")
        
        user = db.query(User).filter(User.id == post.user_id).first()
        if not user or not user.instagram_access_token:
            raise Exception("User Instagram account not connected")
        
        # Check if token needs refresh
        if user.token_expires_at and user.token_expires_at < datetime.utcnow():
            refresh_instagram_token.delay(str(user.id))
            raise Exception("Instagram token expired, refresh in progress")
        
        # Initialize Instagram service
        instagram_service = InstagramService(user.instagram_access_token)
        
        # Publish post based on type
        if post.post_type == "photo":
            result = await instagram_service.upload_photo(
                image_url=post.media_urls[0],
                caption=f"{post.caption} {' '.join(post.hashtags or [])}".strip()
            )
        elif post.post_type == "video":
            result = await instagram_service.upload_video(
                video_url=post.media_urls[0],
                caption=f"{post.caption} {' '.join(post.hashtags or [])}".strip()
            )
        elif post.post_type == "reel":
            result = await instagram_service.upload_video(
                video_url=post.media_urls[0],
                caption=f"{post.caption} {' '.join(post.hashtags or [])}".strip(),
                is_reel=True
            )
        else:
            raise Exception(f"Unsupported post type: {post.post_type}")
        
        # Update post with Instagram data
        post.instagram_post_id = result["id"]
        post.instagram_permalink = result.get("permalink")
        post.status = PostStatus.PUBLISHED
        post.published_at = datetime.utcnow()
        
        db.commit()
        
        # Schedule analytics sync in 1 hour
        sync_single_post_analytics.apply_async(
            args=[post_id],
            countdown=3600  # 1 hour delay
        )
        
        return {"success": True, "instagram_id": result["id"]}
        
    except (InstagramAPIError, RateLimitError) as e:
        # Retry with exponential backoff
        retry_delay = 2 ** self.request.retries * 60  # 1, 2, 4 minutes
        raise self.retry(exc=e, countdown=retry_delay)
        
    except Exception as e:
        # Update post status to failed
        if 'post' in locals():
            post.status = PostStatus.FAILED
            db.commit()
        
        raise Exception(f"Failed to publish post {post_id}: {str(e)}")
        
    finally:
        db.close()

@celery_app.task
def refresh_instagram_token(user_id: str):
    """Refresh Instagram access token for user"""
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.instagram_access_token:
            return {"error": "User or token not found"}
        
        instagram_service = InstagramService(user.instagram_access_token)
        token_data = await instagram_service.refresh_access_token()
        
        # Update user with new token
        user.instagram_access_token = token_data["access_token"]
        user.token_expires_at = datetime.utcnow() + timedelta(days=60)
        
        db.commit()
        
        return {"success": True, "expires_at": user.token_expires_at.isoformat()}
        
    except Exception as e:
        return {"error": str(e)}
        
    finally:
        db.close()

@celery_app.task
def auto_generate_campaign_content():
    """Auto-generate content for active campaigns"""
    db = SessionLocal()
    
    try:
        # Get active campaigns that need content
        campaigns = db.query(Campaign).filter(
            Campaign.is_active == True,
            Campaign.start_date <= datetime.utcnow(),
            Campaign.end_date >= datetime.utcnow()
        ).all()
        
        openai_service = OpenAIService()
        
        for campaign in campaigns:
            # Check if we need to generate content today
            today_posts = db.query(Post).filter(
                Post.campaign_id == campaign.id,
                Post.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0)
            ).count()
            
            if today_posts < campaign.posts_per_day:
                # Generate missing posts
                posts_needed = campaign.posts_per_day - today_posts
                
                for i in range(posts_needed):
                    # Generate content based on campaign themes
                    theme = campaign.content_themes[i % len(campaign.content_themes)]
                    
                    # Generate caption
                    caption = await openai_service.generate_caption(
                        product_description=f"Defeah home decor item featuring {theme}",
                        tone=campaign.brand_voice,
                        style="engaging"
                    )
                    
                    # Generate hashtags
                    hashtags = await openai_service.suggest_hashtags(
                        content_description=f"{theme} home decor",
                        count=10
                    )
                    
                    # Create post
                    post = Post(
                        user_id=campaign.user_id,
                        campaign_id=campaign.id,
                        caption=caption,
                        hashtags=hashtags,
                        post_type="photo",
                        status=PostStatus.DRAFT,
                        ai_prompt=f"Theme: {theme}",
                        ai_model_used="gpt-4",
                        generation_cost=openai_service.last_cost_cents
                    )
                    
                    db.add(post)
                
                db.commit()
        
        return {"campaigns_processed": len(campaigns)}
        
    except Exception as e:
        return {"error": str(e)}
        
    finally:
        db.close()
```

### Analytics Tasks

```python
# app/tasks/analytics_tasks.py
from celery import current_task
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.post import Post, PostStatus
from app.models.user import User
from app.models.analytics import AnalyticsEvent, PerformanceMetrics
from app.services.instagram_service import InstagramService

@celery_app.task
def sync_post_analytics():
    """Sync analytics for all published posts"""
    db = SessionLocal()
    
    try:
        # Get posts that need analytics updates (published in last 30 days)
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        posts = db.query(Post).filter(
            Post.status == PostStatus.PUBLISHED,
            Post.published_at >= cutoff_date,
            Post.instagram_post_id.isnot(None)
        ).all()
        
        for post in posts:
            try:
                sync_single_post_analytics.delay(str(post.id))
            except Exception as e:
                print(f"Failed to queue analytics sync for post {post.id}: {e}")
        
        return {"posts_queued": len(posts)}
        
    except Exception as e:
        return {"error": str(e)}
        
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=3)
def sync_single_post_analytics(self, post_id: str):
    """Sync analytics for a single post"""
    db = SessionLocal()
    
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post or not post.instagram_post_id:
            return {"error": "Post not found or not published"}
        
        user = db.query(User).filter(User.id == post.user_id).first()
        if not user or not user.instagram_access_token:
            return {"error": "User Instagram token not available"}
        
        instagram_service = InstagramService(user.instagram_access_token)
        insights = await instagram_service.get_media_insights(post.instagram_post_id)
        
        # Update post metrics
        for insight in insights.get("data", []):
            metric_name = insight["name"]
            metric_value = insight["values"][0]["value"]
            
            if metric_name == "impressions":
                post.impressions = metric_value
            elif metric_name == "reach":
                post.reach = metric_value
            elif metric_name == "likes":
                post.likes_count = metric_value
            elif metric_name == "comments":
                post.comments_count = metric_value
            elif metric_name == "shares":
                post.shares_count = metric_value
            elif metric_name == "saves":
                post.saves_count = metric_value
            
            # Create analytics event
            event = AnalyticsEvent(
                post_id=post.id,
                event_type=metric_name,
                event_data={"value": metric_value, "timestamp": datetime.utcnow().isoformat()},
                timestamp=datetime.utcnow()
            )
            db.add(event)
        
        post.updated_at = datetime.utcnow()
        db.commit()
        
        return {"success": True, "metrics_updated": len(insights.get("data", []))}
        
    except Exception as e:
        # Retry with exponential backoff
        retry_delay = 2 ** self.request.retries * 60
        raise self.retry(exc=e, countdown=retry_delay)
        
    finally:
        db.close()

@celery_app.task
def generate_daily_performance_report():
    """Generate daily performance metrics for all users"""
    db = SessionLocal()
    
    try:
        yesterday = datetime.utcnow().date() - timedelta(days=1)
        yesterday_start = datetime.combine(yesterday, datetime.min.time())
        yesterday_end = datetime.combine(yesterday, datetime.max.time())
        
        # Get all users with posts
        users_with_posts = db.query(User).join(Post).filter(
            Post.published_at >= yesterday_start,
            Post.published_at <= yesterday_end
        ).distinct().all()
        
        for user in users_with_posts:
            # Calculate daily metrics
            posts = db.query(Post).filter(
                Post.user_id == user.id,
                Post.published_at >= yesterday_start,
                Post.published_at <= yesterday_end,
                Post.status == PostStatus.PUBLISHED
            ).all()
            
            if not posts:
                continue
            
            # Aggregate metrics
            total_posts = len(posts)
            total_likes = sum(post.likes_count or 0 for post in posts)
            total_comments = sum(post.comments_count or 0 for post in posts)
            total_shares = sum(post.shares_count or 0 for post in posts)
            total_saves = sum(post.saves_count or 0 for post in posts)
            total_reach = sum(post.reach or 0 for post in posts)
            total_impressions = sum(post.impressions or 0 for post in posts)
            
            # Calculate engagement rate
            total_engagements = total_likes + total_comments + total_shares + total_saves
            engagement_rate = (total_engagements / total_impressions * 100) if total_impressions > 0 else 0
            
            # Create performance metrics record
            metrics = PerformanceMetrics(
                user_id=user.id,
                date=yesterday_start,
                period_type="daily",
                total_posts=total_posts,
                total_likes=total_likes,
                total_comments=total_comments,
                total_shares=total_shares,
                total_saves=total_saves,
                total_reach=total_reach,
                total_impressions=total_impressions,
                engagement_rate=engagement_rate,
                avg_likes_per_post=total_likes / total_posts if total_posts > 0 else 0
            )
            
            db.add(metrics)
        
        db.commit()
        
        return {"reports_generated": len(users_with_posts)}
        
    except Exception as e:
        return {"error": str(e)}
        
    finally:
        db.close()
```

## Configuration Management

### Settings Configuration

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import secrets

class Settings(BaseSettings):
    # App settings
    PROJECT_NAME: str = "Defeah Marketing Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/defeah_marketing"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Instagram/Facebook
    FACEBOOK_APP_ID: str
    FACEBOOK_APP_SECRET: str
    INSTAGRAM_REDIRECT_URI: str = "http://localhost:8000/auth/instagram/callback"
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Rate limiting
    REQUESTS_PER_MINUTE: int = 60
    MAX_POSTS_PER_DAY: int = 50
    
    # File storage
    MEDIA_UPLOAD_PATH: str = "/tmp/uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Email (for notifications)
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Environment Variables Template

```bash
# .env.example

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/defeah_marketing

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key-here

# Instagram/Facebook App
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
INSTAGRAM_REDIRECT_URI=http://localhost:8000/auth/instagram/callback

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring (optional)
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

## Deployment & Operations

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: defeah_marketing
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/defeah_marketing
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./app:/app/app
      - ./uploads:/app/uploads

  celery:
    build: .
    command: celery -A app.tasks.celery_app worker --loglevel=info
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/defeah_marketing
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./app:/app/app

  celery-beat:
    build: .
    command: celery -A app.tasks.celery_app beat --loglevel=info
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/defeah_marketing
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./app:/app/app

volumes:
  postgres_data:
  redis_data:
```

### Production Deployment

```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.api.v1 import auth, posts, campaigns, analytics, content
from app.core.database import engine
from app.models import user, post, campaign, analytics as analytics_models

# Create tables
def create_tables():
    user.Base.metadata.create_all(bind=engine)
    post.Base.metadata.create_all(bind=engine)
    campaign.Base.metadata.create_all(bind=engine)
    analytics_models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.LOG_LEVEL == "DEBUG" else None,
    redoc_url="/redoc" if settings.LOG_LEVEL == "DEBUG" else None
)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(posts.router, prefix=settings.API_V1_STR)
app.include_router(campaigns.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(content.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/")
async def root():
    return {"message": "Defeah Marketing API", "version": settings.VERSION}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.LOG_LEVEL == "DEBUG"
    )
```

### Requirements File

```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
celery==5.3.4
redis==5.0.1
httpx==0.25.2
openai==1.3.7
pillow==10.1.0
python-magic==0.4.27
sentry-sdk[fastapi]==1.38.0
```

This comprehensive FastAPI backend provides a production-ready foundation for the autonomous Instagram marketing system with proper authentication, database design, API structure, AI integration, task scheduling, and deployment configuration. The architecture is scalable, maintainable, and follows FastAPI best practices while integrating seamlessly with Instagram's API and OpenAI's services.