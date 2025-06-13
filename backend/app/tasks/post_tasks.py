"""
Celery tasks for post management and publishing.
"""
from celery import current_task
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import logging

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.post import Post, PostStatus
from app.models.user import User
from app.models.campaign import Campaign
from app.services.instagram_service import InstagramService
from app.services.openai_service import OpenAIService
from app.utils.exceptions import InstagramAPIException

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def schedule_post_publication(self, post_id: str):
    """Publish a scheduled post to Instagram."""
    db = SessionLocal()
    
    try:
        # Get post and user
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logger.error(f"Post {post_id} not found")
            return {"error": f"Post {post_id} not found"}
        
        user = db.query(User).filter(User.id == post.user_id).first()
        if not user or not user.instagram_access_token:
            logger.error(f"User Instagram account not connected for post {post_id}")
            return {"error": "User Instagram account not connected"}
        
        # Check if token needs refresh
        if user.token_expires_at and user.token_expires_at < datetime.utcnow():
            logger.info(f"Refreshing Instagram token for user {user.id}")
            refresh_instagram_token.delay(str(user.id))
            raise Exception("Instagram token expired, refresh in progress")
        
        # Initialize Instagram service
        instagram_service = InstagramService(user.instagram_access_token)
        
        # Prepare caption with hashtags
        full_caption = post.caption
        if post.hashtags:
            full_caption += "\n\n" + " ".join(post.hashtags)
        
        # Publish post based on type
        try:
            if post.post_type == "photo":
                result = await instagram_service.upload_photo(
                    image_url=post.media_urls[0],
                    caption=full_caption
                )
            elif post.post_type == "video":
                result = await instagram_service.upload_video(
                    video_url=post.media_urls[0],
                    caption=full_caption
                )
            elif post.post_type == "reel":
                result = await instagram_service.upload_video(
                    video_url=post.media_urls[0],
                    caption=full_caption,
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
            
            logger.info(f"Successfully published post {post_id} to Instagram")
            
            # Schedule analytics sync in 1 hour
            sync_single_post_analytics.apply_async(
                args=[post_id],
                countdown=3600  # 1 hour delay
            )
            
            return {"success": True, "instagram_id": result["id"]}
            
        except Exception as e:
            logger.error(f"Failed to publish post {post_id}: {str(e)}")
            
            # Update post status to failed
            post.status = PostStatus.FAILED
            db.commit()
            
            # Retry with exponential backoff
            if self.request.retries < self.max_retries:
                retry_delay = 2 ** self.request.retries * 60  # 1, 2, 4 minutes
                raise self.retry(exc=e, countdown=retry_delay)
            else:
                return {"error": f"Failed to publish post after {self.max_retries} retries: {str(e)}"}
        
    except Exception as e:
        logger.error(f"Error in schedule_post_publication: {str(e)}")
        return {"error": str(e)}
        
    finally:
        db.close()


@celery_app.task
def refresh_instagram_token(user_id: str):
    """Refresh Instagram access token for user."""
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.instagram_access_token:
            return {"error": "User or token not found"}
        
        instagram_service = InstagramService(user.instagram_access_token)
        token_data = await instagram_service.refresh_access_token()
        
        # Update user with new token
        user.instagram_access_token = token_data["access_token"]
        user.token_expires_at = token_data["expires_at"]
        
        db.commit()
        
        logger.info(f"Successfully refreshed Instagram token for user {user_id}")
        
        return {"success": True, "expires_at": token_data["expires_at"].isoformat()}
        
    except Exception as e:
        logger.error(f"Failed to refresh token for user {user_id}: {str(e)}")
        return {"error": str(e)}
        
    finally:
        db.close()


@celery_app.task
def auto_generate_campaign_content():
    """Auto-generate content for active campaigns."""
    db = SessionLocal()
    
    try:
        # Get active campaigns that need content
        campaigns = db.query(Campaign).filter(
            Campaign.is_active == True,
            Campaign.start_date <= datetime.utcnow(),
            Campaign.end_date >= datetime.utcnow()
        ).all()
        
        logger.info(f"Found {len(campaigns)} active campaigns")
        
        openai_service = OpenAIService()
        campaigns_processed = 0
        
        for campaign in campaigns:
            try:
                # Check if we need to generate content today
                today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                today_posts = db.query(Post).filter(
                    Post.campaign_id == campaign.id,
                    Post.created_at >= today_start
                ).count()
                
                if today_posts < campaign.posts_per_day:
                    # Generate missing posts
                    posts_needed = campaign.posts_per_day - today_posts
                    
                    logger.info(f"Generating {posts_needed} posts for campaign {campaign.name}")
                    
                    for i in range(posts_needed):
                        # Select theme (cycle through available themes)
                        themes = campaign.content_themes or ["modern_living"]
                        theme = themes[i % len(themes)]
                        
                        # Generate caption
                        caption = await openai_service.generate_caption(
                            product_description=f"Defeah home decor item featuring {theme}",
                            tone=campaign.brand_voice or "professional",
                            style="engaging",
                            include_hashtags=False  # We'll add hashtags separately
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
                            media_urls=["https://example.com/placeholder.jpg"],  # Placeholder
                            post_type="photo",
                            status=PostStatus.DRAFT,
                            ai_prompt=f"Theme: {theme}",
                            ai_model_used="gpt-4",
                            generation_cost=openai_service.last_cost_cents
                        )
                        
                        db.add(post)
                        
                        # Update campaign spent amount
                        campaign.add_spent_amount(openai_service.last_cost_cents)
                    
                    db.commit()
                    campaigns_processed += 1
                    
                    logger.info(f"Generated {posts_needed} posts for campaign {campaign.name}")
                
            except Exception as e:
                logger.error(f"Error generating content for campaign {campaign.id}: {str(e)}")
                continue
        
        return {"campaigns_processed": campaigns_processed}
        
    except Exception as e:
        logger.error(f"Error in auto_generate_campaign_content: {str(e)}")
        return {"error": str(e)}
        
    finally:
        db.close()


@celery_app.task
def sync_single_post_analytics(post_id: str):
    """Sync analytics for a single post."""
    # This will be implemented in analytics_tasks.py
    pass