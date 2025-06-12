# Defeah Marketing Platform - Development Documentation

## Table of Contents
1. [Development Environment Setup](#development-environment-setup)
2. [Project Architecture](#project-architecture)
3. [Code Standards & Conventions](#code-standards--conventions)
4. [Development Workflow](#development-workflow)
5. [Backend Development](#backend-development)
6. [Frontend Development](#frontend-development)
7. [Database Development](#database-development)
8. [Testing Guidelines](#testing-guidelines)
9. [Debugging & Troubleshooting](#debugging--troubleshooting)
10. [Performance Guidelines](#performance-guidelines)
11. [Security Guidelines](#security-guidelines)
12. [Contributing Guidelines](#contributing-guidelines)

## Development Environment Setup

### Prerequisites

#### Required Software
```bash
# System requirements
- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL 15+
- Redis 7.0+
- Docker & Docker Compose
- Git

# Recommended tools
- VS Code with extensions
- pgAdmin or DBeaver
- Redis CLI
- Postman or Insomnia
```

#### Environment Variables
Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/defeah_dev
TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/defeah_test

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Instagram/Facebook
FACEBOOK_APP_ID=your-dev-app-id
FACEBOOK_APP_SECRET=your-dev-app-secret
INSTAGRAM_REDIRECT_URI=http://localhost:3000/auth/instagram/callback

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Email (optional for development)
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=""
SMTP_PASSWORD=""

# Development settings
DEBUG=true
LOG_LEVEL=DEBUG
ENVIRONMENT=development
```

### Local Development Setup

#### 1. Clone and Setup Backend
```bash
# Clone repository
git clone https://github.com/yourusername/defeah-marketing.git
cd defeah-marketing

# Setup Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

#### 2. Setup Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 3. Docker Development Environment
```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

#### 4. Database Setup
```bash
# Create development database
createdb defeah_dev
createdb defeah_test

# Run migrations
alembic upgrade head

# Seed development data (optional)
python scripts/seed_dev_data.py
```

### VS Code Setup

#### Recommended Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.flake8",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode-remote.remote-containers"
  ]
}
```

#### VS Code Settings
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

## Project Architecture

### Directory Structure
```
defeah-marketing/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── core/
│   │   │   ├── config.py          # Configuration
│   │   │   ├── database.py        # Database connection
│   │   │   ├── redis.py           # Redis connection
│   │   │   └── security.py        # Security utilities
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── api/                   # API routes
│   │   ├── services/              # Business logic
│   │   ├── tasks/                 # Celery tasks
│   │   └── utils/                 # Utility functions
│   ├── migrations/                # Alembic migrations
│   ├── tests/                     # Test suite
│   ├── scripts/                   # Development scripts
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── pages/                 # Page components
│   │   ├── hooks/                 # Custom hooks
│   │   ├── store/                 # Redux store
│   │   ├── services/              # API services
│   │   ├── utils/                 # Utility functions
│   │   └── types/                 # TypeScript types
│   ├── public/                    # Static assets
│   └── package.json
├── docs/                          # Documentation
├── docker-compose.yml             # Production compose
├── docker-compose.dev.yml         # Development compose
└── README.md
```

### Architecture Principles

#### Backend Architecture
- **Clean Architecture**: Separation of concerns with clear layers
- **Domain-Driven Design**: Business logic organized by domain
- **Dependency Injection**: Loose coupling between components
- **Event-Driven**: Asynchronous processing with Celery
- **API-First**: RESTful API design with OpenAPI documentation

#### Frontend Architecture
- **Component-Based**: Reusable UI components
- **State Management**: Centralized state with Redux Toolkit
- **Type Safety**: Full TypeScript coverage
- **Responsive Design**: Mobile-first approach
- **Performance**: Code splitting and lazy loading

## Code Standards & Conventions

### Python Code Standards

#### Naming Conventions
```python
# Variables and functions: snake_case
user_name = "john_doe"
def get_user_posts(user_id: int) -> List[Post]:
    pass

# Classes: PascalCase
class UserService:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_POSTS_PER_DAY = 50
DATABASE_URL = "postgresql://..."

# Private methods: leading underscore
def _validate_instagram_token(token: str) -> bool:
    pass
```

#### Import Organization
```python
# Standard library imports
import os
import uuid
from datetime import datetime
from typing import List, Optional

# Third-party imports
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import openai

# Local imports
from app.core.database import get_db
from app.models.user import User
from app.schemas.post import PostCreate
from app.services.instagram_service import InstagramService
```

#### Function Documentation
```python
def generate_instagram_caption(
    product_description: str,
    tone: str = "professional",
    max_length: int = 2200
) -> str:
    """
    Generate Instagram caption using OpenAI API.
    
    Args:
        product_description: Description of the product
        tone: Tone of voice (professional, casual, luxury)
        max_length: Maximum character count for caption
        
    Returns:
        Generated caption text
        
    Raises:
        OpenAIError: If API call fails
        ValidationError: If inputs are invalid
        
    Example:
        >>> caption = generate_instagram_caption(
        ...     "Modern oak coffee table",
        ...     tone="professional"
        ... )
        >>> len(caption) <= 2200
        True
    """
    pass
```

#### Error Handling
```python
# Custom exceptions
class InstagramAPIError(Exception):
    """Raised when Instagram API call fails."""
    pass

# Proper error handling
def post_to_instagram(post_data: dict) -> dict:
    try:
        response = instagram_client.create_post(post_data)
        return response
    except requests.HTTPError as e:
        if e.response.status_code == 429:
            raise InstagramAPIError("Rate limit exceeded")
        elif e.response.status_code == 401:
            raise InstagramAPIError("Invalid credentials")
        else:
            raise InstagramAPIError(f"API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error posting to Instagram: {e}")
        raise
```

### TypeScript Code Standards

#### Naming Conventions
```typescript
// Variables and functions: camelCase
const userName = 'john_doe';
const getUserPosts = (userId: number): Post[] => [];

// Interfaces and types: PascalCase
interface User {
  id: string;
  email: string;
  createdAt: string;
}

type PostStatus = 'draft' | 'scheduled' | 'published' | 'failed';

// Constants: UPPER_SNAKE_CASE
const MAX_POSTS_PER_DAY = 50;
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

#### Component Structure
```typescript
// Component props interface
interface PostCardProps {
  post: Post;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  className?: string;
}

// Component with proper typing
export const PostCard: React.FC<PostCardProps> = ({
  post,
  onEdit,
  onDelete,
  className = ''
}) => {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleEdit = useCallback(() => {
    onEdit(post.id);
  }, [post.id, onEdit]);
  
  return (
    <div className={`post-card ${className}`}>
      {/* Component content */}
    </div>
  );
};
```

#### API Service Pattern
```typescript
// API service with proper error handling
class PostsAPI {
  private baseURL = '/api/v1/posts';
  
  async getPosts(params?: GetPostsParams): Promise<PostsResponse> {
    try {
      const response = await fetch(`${this.baseURL}?${new URLSearchParams(params)}`);
      
      if (!response.ok) {
        throw new APIError(response.status, await response.text());
      }
      
      return response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(500, 'Network error');
    }
  }
}
```

### Git Commit Standards

#### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

#### Examples
```bash
feat(auth): add Instagram OAuth integration

- Implement OAuth flow for Instagram login
- Add token refresh mechanism
- Update user model to store Instagram credentials

Closes #123

fix(api): handle rate limiting errors properly

- Add exponential backoff for Instagram API calls
- Return user-friendly error messages
- Log rate limit events for monitoring

Fixes #456
```

## Development Workflow

### Branch Strategy

#### Git Flow
```bash
main           # Production-ready code
├── develop    # Integration branch for features
├── feature/*  # Feature development branches
├── release/*  # Release preparation branches
└── hotfix/*   # Emergency fixes for production
```

#### Branch Naming
```bash
feature/auth-instagram-integration
feature/post-scheduling-ui
fix/instagram-api-rate-limiting
hotfix/security-token-validation
release/v1.2.0
```

### Development Process

#### 1. Feature Development
```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/new-feature-name

# Development work
# ... make changes ...

# Commit changes
git add .
git commit -m "feat(feature): implement new feature"

# Push and create PR
git push origin feature/new-feature-name
# Create Pull Request on GitHub/GitLab
```

#### 2. Code Review Process
- **All code must be reviewed** before merging
- **Automated checks must pass**: linting, tests, security scans
- **Review checklist**:
  - Code follows style guidelines
  - Tests are included and passing
  - Documentation is updated
  - No security vulnerabilities
  - Performance considerations addressed

#### 3. Testing Requirements
```bash
# Run all tests before committing
npm run test                    # Frontend tests
pytest                         # Backend tests
pytest --cov=app tests/        # Backend tests with coverage

# Run linting
npm run lint                    # Frontend linting
flake8 app/                    # Backend linting
black --check app/             # Code formatting check
```

### Local Development Commands

#### Backend Commands
```bash
# Start development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest
pytest -v                      # Verbose output
pytest tests/test_posts.py     # Specific test file
pytest -k "test_create_post"   # Specific test

# Database operations
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
alembic downgrade -1

# Celery worker
celery -A app.tasks.celery_app worker --loglevel=info
celery -A app.tasks.celery_app beat --loglevel=info

# Code quality
black app/                     # Format code
isort app/                     # Sort imports
flake8 app/                    # Linting
mypy app/                      # Type checking
```

#### Frontend Commands
```bash
# Start development server
npm run dev

# Run tests
npm run test
npm run test:watch             # Watch mode
npm run test:coverage          # With coverage

# Build for production
npm run build
npm run preview                # Preview build

# Code quality
npm run lint                   # ESLint
npm run lint:fix               # Fix linting issues
npm run type-check             # TypeScript checking
npm run format                 # Prettier formatting
```

## Backend Development

### FastAPI Development Patterns

#### Router Organization
```python
# app/api/v1/posts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.post import PostCreate, PostResponse
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post."""
    post_service = PostService(db)
    return await post_service.create_post(post_data, current_user.id)
```

#### Service Layer Pattern
```python
# app/services/post_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

class PostService:
    def __init__(self, db: Session):
        self.db = db
        
    async def create_post(self, post_data: PostCreate, user_id: str) -> Post:
        """Create a new post."""
        db_post = Post(
            user_id=user_id,
            **post_data.dict()
        )
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post
        
    async def get_posts(
        self, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Post]:
        """Get posts for a user."""
        return self.db.query(Post)\
            .filter(Post.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
```

#### Database Models
```python
# app/models/post.py
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    caption = Column(Text)
    hashtags = Column(ARRAY(String(50)))
    media_urls = Column(ARRAY(Text))
    
    status = Column(String(20), default="draft")
    scheduled_time = Column(DateTime)
    published_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="posts")
```

#### Pydantic Schemas
```python
# app/schemas/post.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from enum import Enum

class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

class PostBase(BaseModel):
    caption: str = Field(..., max_length=2200)
    hashtags: Optional[List[str]] = Field(default=[], max_items=30)
    media_urls: List[str] = Field(..., min_items=1, max_items=10)
    
    @validator('hashtags')
    def validate_hashtags(cls, v):
        if v:
            for hashtag in v:
                if not hashtag.startswith('#'):
                    raise ValueError('Hashtags must start with #')
        return v

class PostCreate(PostBase):
    scheduled_time: Optional[datetime] = None

class PostResponse(PostBase):
    id: str
    status: PostStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

### Celery Task Development

#### Task Definition
```python
# app/tasks/post_tasks.py
from celery import current_task
from app.tasks.celery_app import celery_app
from app.services.instagram_service import InstagramService

@celery_app.task(bind=True, max_retries=3)
def publish_post_to_instagram(self, post_id: str):
    """Publish a scheduled post to Instagram."""
    try:
        # Get post from database
        # Publish to Instagram
        # Update post status
        pass
    except Exception as exc:
        # Exponential backoff retry
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

@celery_app.task
def sync_post_analytics():
    """Sync analytics for all published posts."""
    # Implementation
    pass
```

#### Task Monitoring
```python
# Check task status
from app.tasks.celery_app import celery_app

result = publish_post_to_instagram.delay(post_id)
print(f"Task ID: {result.id}")
print(f"Status: {result.status}")
print(f"Result: {result.result}")
```

## Frontend Development

### React Component Patterns

#### Component Structure
```typescript
// src/components/posts/PostCard.tsx
import React, { useState, useCallback } from 'react';
import { Post } from '../../types/post';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';

interface PostCardProps {
  post: Post;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  className?: string;
}

export const PostCard: React.FC<PostCardProps> = ({
  post,
  onEdit,
  onDelete,
  className = ''
}) => {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleEdit = useCallback(() => {
    onEdit(post.id);
  }, [post.id, onEdit]);
  
  const handleDelete = useCallback(async () => {
    if (window.confirm('Are you sure you want to delete this post?')) {
      setIsLoading(true);
      try {
        await onDelete(post.id);
      } finally {
        setIsLoading(false);
      }
    }
  }, [post.id, onDelete]);
  
  return (
    <div className={`post-card ${className}`}>
      <div className="post-card-header">
        <h3 className="post-title">{post.caption.substring(0, 50)}...</h3>
        <Badge variant={post.status}>{post.status}</Badge>
      </div>
      
      <div className="post-card-content">
        <p className="post-caption">{post.caption}</p>
        <div className="post-hashtags">
          {post.hashtags.map(tag => (
            <span key={tag} className="hashtag">{tag}</span>
          ))}
        </div>
      </div>
      
      <div className="post-card-actions">
        <Button onClick={handleEdit} variant="outline">
          Edit
        </Button>
        <Button 
          onClick={handleDelete} 
          variant="destructive"
          loading={isLoading}
        >
          Delete
        </Button>
      </div>
    </div>
  );
};
```

#### Custom Hooks
```typescript
// src/hooks/usePosts.ts
import { useState, useEffect, useCallback } from 'react';
import { Post, CreatePostRequest } from '../types/post';
import { postsAPI } from '../services/api';

interface UsePostsResult {
  posts: Post[];
  loading: boolean;
  error: string | null;
  createPost: (data: CreatePostRequest) => Promise<void>;
  updatePost: (id: string, data: Partial<Post>) => Promise<void>;
  deletePost: (id: string) => Promise<void>;
  refetch: () => void;
}

export const usePosts = (): UsePostsResult => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const fetchPosts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await postsAPI.getPosts();
      setPosts(response.posts);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);
  
  const createPost = useCallback(async (data: CreatePostRequest) => {
    const newPost = await postsAPI.createPost(data);
    setPosts(prev => [newPost, ...prev]);
  }, []);
  
  const updatePost = useCallback(async (id: string, data: Partial<Post>) => {
    const updatedPost = await postsAPI.updatePost(id, data);
    setPosts(prev => prev.map(post => post.id === id ? updatedPost : post));
  }, []);
  
  const deletePost = useCallback(async (id: string) => {
    await postsAPI.deletePost(id);
    setPosts(prev => prev.filter(post => post.id !== id));
  }, []);
  
  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);
  
  return {
    posts,
    loading,
    error,
    createPost,
    updatePost,
    deletePost,
    refetch: fetchPosts
  };
};
```

### State Management with Redux

#### Store Configuration
```typescript
// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { postsAPI } from './api/postsAPI';
import authSlice from './slices/authSlice';
import uiSlice from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    ui: uiSlice,
    [postsAPI.reducerPath]: postsAPI.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(postsAPI.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

#### RTK Query API
```typescript
// src/store/api/postsAPI.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { Post, CreatePostRequest, PostsResponse } from '../../types/post';

export const postsAPI = createApi({
  reducerPath: 'postsAPI',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api/v1/posts',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Post'],
  endpoints: (builder) => ({
    getPosts: builder.query<PostsResponse, void>({
      query: () => '',
      providesTags: ['Post'],
    }),
    createPost: builder.mutation<Post, CreatePostRequest>({
      query: (post) => ({
        url: '',
        method: 'POST',
        body: post,
      }),
      invalidatesTags: ['Post'],
    }),
    updatePost: builder.mutation<Post, { id: string; data: Partial<Post> }>({
      query: ({ id, data }) => ({
        url: `/${id}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: ['Post'],
    }),
    deletePost: builder.mutation<void, string>({
      query: (id) => ({
        url: `/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Post'],
    }),
  }),
});

export const {
  useGetPostsQuery,
  useCreatePostMutation,
  useUpdatePostMutation,
  useDeletePostMutation,
} = postsAPI;
```

## Database Development

### Migration Management

#### Creating Migrations
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add post analytics table"

# Create empty migration for data changes
alembic revision -m "Migrate old post data"

# Review generated migration before applying
# Edit migration file if needed

# Apply migration
alembic upgrade head
```

#### Migration Best Practices
```python
# migrations/versions/001_add_post_analytics.py
"""Add post analytics table

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_analytics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('post_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('likes_count', sa.Integer(), nullable=True),
        sa.Column('comments_count', sa.Integer(), nullable=True),
        sa.Column('shares_count', sa.Integer(), nullable=True),
        sa.Column('reach', sa.Integer(), nullable=True),
        sa.Column('impressions', sa.Integer(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_post_analytics_post_id', 'post_analytics', ['post_id'])
    op.create_index('ix_post_analytics_recorded_at', 'post_analytics', ['recorded_at'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_post_analytics_recorded_at', table_name='post_analytics')
    op.drop_index('ix_post_analytics_post_id', table_name='post_analytics')
    op.drop_table('post_analytics')
    # ### end Alembic commands ###
```

### Database Queries

#### Efficient Queries
```python
# Good: Use joins to avoid N+1 queries
def get_posts_with_user(db: Session) -> List[Post]:
    return db.query(Post)\
        .join(User)\
        .options(joinedload(Post.user))\
        .all()

# Good: Use pagination
def get_posts_paginated(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[Post]:
    return db.query(Post)\
        .offset(skip)\
        .limit(limit)\
        .all()

# Good: Use indexes for filtering
def get_posts_by_status(db: Session, status: str) -> List[Post]:
    return db.query(Post)\
        .filter(Post.status == status)\
        .all()
```

#### Raw SQL for Complex Queries
```python
from sqlalchemy import text

def get_engagement_analytics(db: Session, user_id: str, days: int = 30):
    """Get engagement analytics for the last N days."""
    query = text("""
        SELECT 
            DATE(p.published_at) as date,
            COUNT(*) as posts_count,
            AVG(p.likes_count) as avg_likes,
            AVG(p.comments_count) as avg_comments,
            AVG(p.reach) as avg_reach
        FROM posts p
        WHERE p.user_id = :user_id
        AND p.published_at >= NOW() - INTERVAL ':days days'
        AND p.status = 'published'
        GROUP BY DATE(p.published_at)
        ORDER BY date DESC
    """)
    
    result = db.execute(query, {"user_id": user_id, "days": days})
    return [dict(row) for row in result]
```

## Testing Guidelines

### Backend Testing

#### Unit Tests
```python
# tests/test_services/test_post_service.py
import pytest
from unittest.mock import Mock, patch
from app.services.post_service import PostService
from app.schemas.post import PostCreate

class TestPostService:
    def test_create_post_success(self, db_session, sample_user):
        """Test successful post creation."""
        service = PostService(db_session)
        post_data = PostCreate(
            caption="Test post",
            hashtags=["#test"],
            media_urls=["https://example.com/image.jpg"]
        )
        
        post = service.create_post(post_data, sample_user.id)
        
        assert post.caption == "Test post"
        assert post.user_id == sample_user.id
        assert post.status == "draft"
    
    def test_create_post_validation_error(self, db_session, sample_user):
        """Test post creation with invalid data."""
        service = PostService(db_session)
        
        with pytest.raises(ValidationError):
            PostCreate(
                caption="",  # Empty caption should fail
                media_urls=[]  # Empty media URLs should fail
            )
```

#### Integration Tests
```python
# tests/test_api/test_posts.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestPostsAPI:
    def test_create_post_endpoint(self, client: TestClient, auth_headers):
        """Test POST /api/v1/posts endpoint."""
        post_data = {
            "caption": "Test post",
            "hashtags": ["#test"],
            "media_urls": ["https://example.com/image.jpg"]
        }
        
        response = client.post(
            "/api/v1/posts",
            json=post_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["caption"] == "Test post"
        assert data["status"] == "draft"
    
    def test_get_posts_endpoint(self, client: TestClient, auth_headers, sample_posts):
        """Test GET /api/v1/posts endpoint."""
        response = client.get("/api/v1/posts", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        assert len(data["posts"]) == len(sample_posts)
```

### Frontend Testing

#### Component Tests
```typescript
// src/components/posts/__tests__/PostCard.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { PostCard } from '../PostCard';
import { mockPost } from '../../../__mocks__/posts';

describe('PostCard', () => {
  const mockOnEdit = jest.fn();
  const mockOnDelete = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('renders post information correctly', () => {
    render(
      <PostCard 
        post={mockPost}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
      />
    );
    
    expect(screen.getByText(mockPost.caption.substring(0, 50))).toBeInTheDocument();
    expect(screen.getByText(mockPost.status)).toBeInTheDocument();
  });
  
  it('calls onEdit when edit button is clicked', () => {
    render(
      <PostCard 
        post={mockPost}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
      />
    );
    
    fireEvent.click(screen.getByText('Edit'));
    expect(mockOnEdit).toHaveBeenCalledWith(mockPost.id);
  });
  
  it('shows confirmation dialog when delete is clicked', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(true);
    
    render(
      <PostCard 
        post={mockPost}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
      />
    );
    
    fireEvent.click(screen.getByText('Delete'));
    
    await waitFor(() => {
      expect(mockOnDelete).toHaveBeenCalledWith(mockPost.id);
    });
  });
});
```

#### Hook Tests
```typescript
// src/hooks/__tests__/usePosts.test.tsx
import { renderHook, act } from '@testing-library/react';
import { usePosts } from '../usePosts';
import { postsAPI } from '../../services/api';

jest.mock('../../services/api');

describe('usePosts', () => {
  it('fetches posts on mount', async () => {
    const mockPosts = [{ id: '1', caption: 'Test post' }];
    (postsAPI.getPosts as jest.Mock).mockResolvedValue({ posts: mockPosts });
    
    const { result } = renderHook(() => usePosts());
    
    expect(result.current.loading).toBe(true);
    
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });
    
    expect(result.current.loading).toBe(false);
    expect(result.current.posts).toEqual(mockPosts);
  });
  
  it('handles errors gracefully', async () => {
    (postsAPI.getPosts as jest.Mock).mockRejectedValue(new Error('API Error'));
    
    const { result } = renderHook(() => usePosts());
    
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });
    
    expect(result.current.error).toBe('API Error');
    expect(result.current.posts).toEqual([]);
  });
});
```

### Test Configuration

#### Pytest Configuration
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
```

#### Jest Configuration
```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "testEnvironment": "jsdom",
    "setupFilesAfterEnv": ["<rootDir>/src/setupTests.ts"],
    "moduleNameMapping": {
      "^@/(.*)$": "<rootDir>/src/$1"
    },
    "collectCoverageFrom": [
      "src/**/*.{js,jsx,ts,tsx}",
      "!src/**/*.d.ts",
      "!src/index.tsx"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## Debugging & Troubleshooting

### Backend Debugging

#### Logging Configuration
```python
# app/core/logging.py
import logging
import sys
from app.core.config import settings

def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log') if settings.ENVIRONMENT != 'development' else logging.NullHandler()
        ]
    )
    
    # Configure third-party loggers
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Usage in code
import logging
logger = logging.getLogger(__name__)

def some_function():
    logger.info("Function called")
    try:
        # Some operation
        pass
    except Exception as e:
        logger.error(f"Operation failed: {e}", exc_info=True)
```

#### Debugging Tools
```python
# Use pdb for debugging
import pdb; pdb.set_trace()

# Use logging for production debugging
logger.debug(f"Processing user {user_id}")
logger.info(f"Post created with ID {post.id}")
logger.warning(f"Rate limit approaching for user {user_id}")
logger.error(f"Failed to post to Instagram: {error}", exc_info=True)
```

### Frontend Debugging

#### Browser Dev Tools
```typescript
// Use console methods for debugging
console.log('Component rendered with props:', props);
console.warn('Deprecated prop used:', propName);
console.error('API call failed:', error);

// Use debugger statement
const handleSubmit = (data: FormData) => {
  debugger; // Execution will pause here
  submitData(data);
};
```

#### React Dev Tools
```typescript
// Add display names for debugging
export const PostCard: React.FC<PostCardProps> = (props) => {
  // Component logic
};
PostCard.displayName = 'PostCard';

// Use React.memo with debug info
export const PostCard = React.memo<PostCardProps>((props) => {
  // Component logic
}, (prevProps, nextProps) => {
  // Custom comparison for debugging
  console.log('PostCard memo comparison:', { prevProps, nextProps });
  return prevProps.post.id === nextProps.post.id;
});
```

### Common Issues and Solutions

#### Database Connection Issues
```python
# Check database connection
from app.core.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")
```

#### Instagram API Issues
```python
# Debug Instagram API calls
import logging
import requests

logger = logging.getLogger(__name__)

def debug_instagram_api(url: str, headers: dict, data: dict):
    """Debug Instagram API calls."""
    logger.debug(f"API URL: {url}")
    logger.debug(f"Headers: {headers}")
    logger.debug(f"Data: {data}")
    
    response = requests.post(url, headers=headers, json=data)
    
    logger.debug(f"Response Status: {response.status_code}")
    logger.debug(f"Response Headers: {response.headers}")
    logger.debug(f"Response Body: {response.text}")
    
    return response
```

## Performance Guidelines

### Backend Performance

#### Database Optimization
```python
# Use database indexes
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(20), default="draft", index=True)
    published_at = Column(DateTime, index=True)

# Use query optimization
def get_user_posts_optimized(db: Session, user_id: str):
    return db.query(Post)\
        .options(joinedload(Post.analytics))\
        .filter(Post.user_id == user_id)\
        .order_by(Post.created_at.desc())\
        .limit(50)\
        .all()

# Use database connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

#### Caching Strategies
```python
# Redis caching
import redis
from functools import wraps

redis_client = redis.Redis.from_url(settings.REDIS_URL)

def cache_result(expire: int = 300):
    """Cache function result in Redis."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Get fresh data
            result = await func(*args, **kwargs)
            
            # Cache result
            redis_client.setex(
                cache_key,
                expire,
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator

@cache_result(expire=600)
async def get_instagram_analytics(user_id: str):
    """Get Instagram analytics with caching."""
    # Expensive operation
    pass
```

### Frontend Performance

#### Component Optimization
```typescript
// Use React.memo for expensive components
export const PostCard = React.memo<PostCardProps>(({ post, onEdit, onDelete }) => {
  // Component logic
}, (prevProps, nextProps) => {
  return prevProps.post.id === nextProps.post.id &&
         prevProps.post.updated_at === nextProps.post.updated_at;
});

// Use useMemo for expensive calculations
const PostsList: React.FC<PostsListProps> = ({ posts, filters }) => {
  const filteredPosts = useMemo(() => {
    return posts.filter(post => {
      if (filters.status && post.status !== filters.status) return false;
      if (filters.search && !post.caption.includes(filters.search)) return false;
      return true;
    });
  }, [posts, filters]);

  return (
    <div>
      {filteredPosts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
};

// Use useCallback for event handlers
const PostsPage: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  
  const handleEdit = useCallback((id: string) => {
    // Edit logic
  }, []);
  
  const handleDelete = useCallback((id: string) => {
    setPosts(prev => prev.filter(post => post.id !== id));
  }, []);
  
  return (
    <div>
      {posts.map(post => (
        <PostCard 
          key={post.id}
          post={post}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
};
```

#### Bundle Optimization
```typescript
// Lazy loading for routes
import { lazy, Suspense } from 'react';

const PostsPage = lazy(() => import('./pages/PostsPage'));
const AnalyticsPage = lazy(() => import('./pages/AnalyticsPage'));

const App: React.FC = () => {
  return (
    <Router>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/posts" element={<PostsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </Suspense>
    </Router>
  );
};

// Code splitting for large libraries
const ChartComponent = lazy(() => 
  import('./components/ChartComponent').then(module => ({
    default: module.ChartComponent
  }))
);
```

## Security Guidelines

### Input Validation
```python
# Backend validation with Pydantic
from pydantic import BaseModel, validator, Field

class PostCreate(BaseModel):
    caption: str = Field(..., max_length=2200)
    hashtags: List[str] = Field(default=[], max_items=30)
    
    @validator('caption')
    def validate_caption(cls, v):
        if not v.strip():
            raise ValueError('Caption cannot be empty')
        return v.strip()
    
    @validator('hashtags')
    def validate_hashtags(cls, v):
        for hashtag in v:
            if not hashtag.startswith('#'):
                raise ValueError('Hashtags must start with #')
            if len(hashtag) > 50:
                raise ValueError('Hashtag too long')
        return v
```

### Authentication Security
```python
# Secure password hashing
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# JWT token security
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Frontend Security
```typescript
// Sanitize user input
import DOMPurify from 'dompurify';

const sanitizeHTML = (html: string): string => {
  return DOMPurify.sanitize(html);
};

// Secure API calls
const apiRequest = async (url: string, options: RequestInit = {}) => {
  const token = localStorage.getItem('access_token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  if (response.status === 401) {
    // Token expired, redirect to login
    localStorage.removeItem('access_token');
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }
  
  return response;
};
```

## Contributing Guidelines

### Code Review Checklist

#### General
- [ ] Code follows project style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No hardcoded values or secrets
- [ ] Error handling is appropriate
- [ ] Performance impact is considered

#### Backend Specific
- [ ] Database migrations are included if needed
- [ ] API endpoints are properly documented
- [ ] Input validation is implemented
- [ ] Logging is appropriate
- [ ] Security considerations are addressed

#### Frontend Specific
- [ ] Components are accessible
- [ ] TypeScript types are properly defined
- [ ] No console.log statements in production code
- [ ] Components are responsive
- [ ] Loading and error states are handled

### Release Process

#### Version Numbering
Follow Semantic Versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

#### Release Steps
```bash
# 1. Create release branch
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# 2. Update version numbers
# Update package.json, __init__.py, etc.

# 3. Update CHANGELOG.md
# Add release notes

# 4. Test thoroughly
npm run test
pytest
npm run build

# 5. Merge to main
git checkout main
git merge release/v1.2.0

# 6. Tag release
git tag v1.2.0
git push origin main --tags

# 7. Deploy to production
# Trigger deployment pipeline

# 8. Merge back to develop
git checkout develop
git merge main
git push origin develop
```

This comprehensive development documentation provides everything needed for developers to contribute effectively to the Defeah Marketing platform while maintaining high code quality and consistency standards.