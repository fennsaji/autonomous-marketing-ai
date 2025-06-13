"""
Posts management API endpoints.
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.post import Post, PostStatus
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostsResponse, PublishResponse
from app.utils.exceptions import PostNotFoundException

router = APIRouter(prefix="/posts")


@router.get("/", response_model=PostsResponse)
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[PostStatus] = Query(None, alias="status"),
    campaign_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's posts with optional filtering."""
    query = db.query(Post).filter(Post.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Post.status == status_filter)
    
    if campaign_id:
        query = query.filter(Post.campaign_id == campaign_id)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    # Calculate pagination info
    page = (skip // limit) + 1
    pages = (total + limit - 1) // limit
    has_next = skip + limit < total
    has_prev = skip > 0
    
    return PostsResponse(
        posts=[PostResponse.from_orm(post) for post in posts],
        total=total,
        page=page,
        pages=pages,
        has_next=has_next,
        has_prev=has_prev
    )


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post."""
    db_post = Post(
        user_id=current_user.id,
        campaign_id=post_data.campaign_id,
        caption=post_data.caption,
        hashtags=post_data.hashtags,
        media_urls=post_data.media_urls,
        post_type=post_data.post_type,
        scheduled_time=post_data.scheduled_time,
        status=PostStatus.SCHEDULED if post_data.scheduled_time else PostStatus.DRAFT
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # TODO: Schedule post for publishing if scheduled_time is provided
    
    return PostResponse.from_orm(db_post)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific post by ID."""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise PostNotFoundException("Post not found")
    
    return PostResponse.from_orm(post)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update existing post."""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise PostNotFoundException("Post not found")
    
    # Update fields
    for field, value in post_update.dict(exclude_unset=True).items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    
    return PostResponse.from_orm(post)


@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a post."""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise PostNotFoundException("Post not found")
    
    db.delete(post)
    db.commit()
    
    return {"message": "Post deleted successfully"}


@router.post("/{post_id}/publish", response_model=PublishResponse)
async def publish_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Publish post immediately to Instagram."""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise PostNotFoundException("Post not found")
    
    # TODO: Implement Instagram publishing logic
    
    return PublishResponse(
        message="Post publishing initiated",
        instagram_post_id="placeholder",
        published_at=post.published_at or post.created_at
    )