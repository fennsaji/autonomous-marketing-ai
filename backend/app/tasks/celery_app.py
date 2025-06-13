"""
Celery application configuration for background tasks.
"""
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "defeah_marketing",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.post_tasks"
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

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    # Refresh Instagram tokens daily at 2 AM
    "refresh-instagram-tokens": {
        "task": "app.tasks.post_tasks.refresh_instagram_tokens",
        "schedule": crontab(hour=2, minute=0),
    },
    
    
    # Auto-generate content for active campaigns at 10 AM
    "auto-generate-content": {
        "task": "app.tasks.post_tasks.auto_generate_campaign_content",
        "schedule": crontab(hour=10, minute=0),
    }
}