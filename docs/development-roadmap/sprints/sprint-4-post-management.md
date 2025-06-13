# Sprint 4: Post Management System
**Duration**: Weeks 7-8 | **Focus**: Complete CRUD Operations & Scheduling

## Sprint Goals

### Primary Objectives
- ✅ Implement comprehensive post management with full CRUD operations
- ✅ Build intelligent post scheduling system with optimal timing
- ✅ Create media upload and processing infrastructure
- ✅ Establish post status tracking and real-time updates
- ✅ Develop content calendar and timeline visualization

### Success Criteria
- [ ] Users can create, edit, update, and delete posts with full version history
- [ ] Post scheduling works with timezone support and optimal timing suggestions
- [ ] Media uploads support multiple formats with automatic optimization
- [ ] Real-time post status updates via WebSocket connections
- [ ] Content calendar provides comprehensive scheduling overview

## Epic Breakdown

### Epic 1: Core Post Management
**Story Points**: 14 | **Priority**: Critical

#### User Stories
1. **POST-001**: As a user, I can create posts with rich content
   - Multi-media support (images, videos, carousels)
   - Caption editing with character count and preview
   - Hashtag management with suggestions and validation
   - Draft saving and version history
   - **Acceptance Criteria**:
     - POST /posts creates new post with validation
     - Support for all Instagram post types (photo, video, carousel, reel)
     - Auto-save functionality prevents content loss
     - Version history tracks all changes

2. **POST-002**: As a user, I can edit and manage existing posts
   - Edit captions, hashtags, and media before publishing
   - Duplicate posts for template creation
   - Bulk operations for multiple posts
   - Delete posts with confirmation and soft deletion
   - **Acceptance Criteria**:
     - PUT /posts/{id} updates post content
     - Soft deletion preserves audit trail
     - Bulk operations support up to 50 posts
     - Template creation from existing posts

3. **POST-003**: As a user, I can organize posts with metadata
   - Tagging and categorization system
   - Custom labels and organization
   - Search and filter functionality
   - Performance tracking and analytics
   - **Acceptance Criteria**:
     - Posts can be tagged with custom labels
     - Advanced search with multiple filters
     - Performance metrics integrated into post data

#### Technical Tasks
- [ ] Implement comprehensive post model with all Instagram post types
- [ ] Create post CRUD endpoints with validation
- [ ] Build version history and audit trail system
- [ ] Add soft deletion and recovery functionality
- [ ] Implement search and filtering with database optimization

### Epic 2: Intelligent Scheduling System
**Story Points**: 12 | **Priority**: Critical

#### User Stories
1. **POST-004**: As a user, I can schedule posts for optimal engagement
   - AI-powered optimal timing suggestions
   - Multiple timezone support
   - Recurring post scheduling
   - Schedule conflict detection and resolution
   - **Acceptance Criteria**:
     - POST /posts/{id}/schedule sets publication time
     - Optimal timing suggestions based on audience analytics
     - Timezone conversion handled automatically
     - Conflict detection prevents double-posting

2. **POST-005**: As a user, I can manage my posting schedule
   - Content calendar view with drag-and-drop
   - Schedule modification and rescheduling
   - Bulk scheduling operations
   - Schedule templates for consistent posting
   - **Acceptance Criteria**:
     - GET /posts/calendar returns organized schedule view
     - Drag-and-drop rescheduling via API
     - Schedule templates reduce manual work
     - Bulk operations support efficient management

3. **POST-006**: As a system, I can execute scheduled posts reliably
   - Background task processing with Celery
   - Retry logic for failed publications
   - Status notifications and updates
   - Schedule monitoring and health checks
   - **Acceptance Criteria**:
     - Scheduled posts publish within 1 minute of target time
     - Failed publications retry with exponential backoff
     - Real-time status updates via WebSocket
     - System health monitoring for scheduler

#### Technical Tasks
- [ ] Build Celery-based scheduling infrastructure
- [ ] Implement optimal timing algorithm using audience data
- [ ] Create timezone handling and conversion system
- [ ] Add schedule conflict detection and resolution
- [ ] Build content calendar API and management tools

### Epic 3: Media Management Infrastructure
**Story Points**: 10 | **Priority**: High

#### User Stories
1. **POST-007**: As a user, I can upload and manage media files
   - Multi-format support (JPEG, PNG, MP4, GIF)
   - Automatic image optimization and resizing
   - Video processing and thumbnail generation
   - Media library with organization and search
   - **Acceptance Criteria**:
     - POST /media/upload handles multiple file formats
     - Images automatically optimized for Instagram (1080x1080)
     - Video thumbnails generated automatically
     - Media library supports tagging and search

2. **POST-008**: As a user, I can edit and enhance media
   - Basic image editing (crop, rotate, filters)
   - Text overlay and branding additions
   - Video trimming and format conversion
   - AI-powered enhancement suggestions
   - **Acceptance Criteria**:
     - Basic editing tools available via API
     - Consistent branding can be applied automatically
     - Video processing handles Instagram requirements
     - AI suggestions improve media quality

3. **POST-009**: As a system, I can optimize media for Instagram
   - Format validation and conversion
   - Size optimization for fast loading
   - Quality validation and enhancement
   - CDN integration for global delivery
   - **Acceptance Criteria**:
     - All uploaded media meets Instagram specifications
     - File sizes optimized for mobile delivery
     - CDN delivers media with <200ms latency globally
     - Quality validation prevents poor uploads

#### Technical Tasks
- [ ] Implement media upload with multi-format support
- [ ] Build image processing pipeline with optimization
- [ ] Create video processing and thumbnail generation
- [ ] Add media library with organization features
- [ ] Integrate CDN for optimized media delivery

### Epic 4: Real-time Status & Notifications
**Story Points**: 8 | **Priority**: High

#### User Stories
1. **POST-010**: As a user, I receive real-time updates on post status
   - Live publishing progress indicators
   - Instant success/failure notifications
   - Post performance updates in real-time
   - Schedule change notifications
   - **Acceptance Criteria**:
     - WebSocket connection provides real-time updates
     - Publishing progress shown with percentage completion
     - Performance metrics update automatically
     - All status changes trigger appropriate notifications

2. **POST-011**: As a user, I can track post performance immediately
   - Real-time engagement metrics (likes, comments, shares)
   - Reach and impression updates
   - Audience interaction notifications
   - Performance comparison with previous posts
   - **Acceptance Criteria**:
     - Engagement metrics update within 5 minutes of changes
     - Performance dashboards reflect real-time data
     - Notifications for significant engagement milestones
     - Historical comparison data readily available

#### Technical Tasks
- [ ] Implement WebSocket infrastructure for real-time updates
- [ ] Build post status tracking and notification system
- [ ] Create real-time analytics data pipeline
- [ ] Add performance monitoring and alerting
- [ ] Implement notification preferences and filtering

### Epic 5: Content Calendar & Planning
**Story Points**: 6 | **Priority**: Medium

#### User Stories
1. **POST-012**: As a user, I can visualize my content schedule
   - Calendar view with monthly, weekly, daily granularity
   - Color-coded posts by type, campaign, or status
   - Drag-and-drop scheduling interface
   - Content gap identification and suggestions
   - **Acceptance Criteria**:
     - GET /calendar returns organized schedule data
     - Multiple view formats (month/week/day) supported
     - Visual indicators for different post types and statuses
     - Gap analysis suggests optimal posting times

2. **POST-013**: As a user, I can plan content strategically
   - Content mix analysis and recommendations
   - Hashtag distribution optimization
   - Performance prediction for scheduled content
   - Campaign timeline integration
   - **Acceptance Criteria**:
     - Content mix analysis identifies posting patterns
     - Hashtag distribution prevents over-use
     - Performance predictions help optimize schedule
     - Campaign integration shows unified timeline

#### Technical Tasks
- [ ] Build calendar data aggregation and visualization API
- [ ] Create content planning and analysis algorithms
- [ ] Implement drag-and-drop scheduling interface backend
- [ ] Add content gap analysis and recommendations
- [ ] Integrate campaign timeline with post calendar

## Detailed Task Breakdown

### Week 1 Tasks (Days 1-5)

#### Day 1: Post Model Enhancement
- [ ] **MODEL-001**: Enhance post model with all Instagram post types
- [ ] **MODEL-002**: Add version history and audit trail tables
- [ ] **MODEL-003**: Implement soft deletion with recovery
- [ ] **MODEL-004**: Create post tagging and categorization system
- [ ] **MODEL-005**: Add post metadata fields for organization

#### Day 2-3: CRUD Operations
- [ ] **CRUD-001**: Implement comprehensive post creation endpoint
- [ ] **CRUD-002**: Build post update functionality with validation
- [ ] **CRUD-003**: Add post duplication and template creation
- [ ] **CRUD-004**: Create bulk operations for multiple posts
- [ ] **CRUD-005**: Implement advanced search and filtering

#### Day 4-5: Media Infrastructure
- [ ] **MEDIA-001**: Set up media upload endpoint with validation
- [ ] **MEDIA-002**: Implement image processing and optimization
- [ ] **MEDIA-003**: Build video processing pipeline
- [ ] **MEDIA-004**: Create media library with organization
- [ ] **MEDIA-005**: Integrate CDN for media delivery

### Week 2 Tasks (Days 6-10)

#### Day 1-2: Scheduling System
- [ ] **SCHEDULE-001**: Build Celery-based post scheduling infrastructure
- [ ] **SCHEDULE-002**: Implement optimal timing algorithm
- [ ] **SCHEDULE-003**: Add timezone handling and conversion
- [ ] **SCHEDULE-004**: Create schedule conflict detection
- [ ] **SCHEDULE-005**: Build recurring post scheduling

#### Day 3: Real-time Features
- [ ] **REALTIME-001**: Implement WebSocket infrastructure
- [ ] **REALTIME-002**: Build post status tracking system
- [ ] **REALTIME-003**: Create real-time notification delivery
- [ ] **REALTIME-004**: Add performance monitoring dashboard
- [ ] **REALTIME-005**: Implement notification preferences

#### Day 4-5: Calendar & Integration
- [ ] **CALENDAR-001**: Build content calendar API
- [ ] **CALENDAR-002**: Create content planning algorithms
- [ ] **CALENDAR-003**: Implement drag-and-drop scheduling backend
- [ ] **CALENDAR-004**: Add content gap analysis
- [ ] **CALENDAR-005**: Integrate with existing AI and Instagram services

## API Endpoints to Deliver

### Post Management
```
GET    /api/v1/posts                      # List posts with filters
POST   /api/v1/posts                      # Create new post
GET    /api/v1/posts/{id}                 # Get specific post
PUT    /api/v1/posts/{id}                 # Update post
DELETE /api/v1/posts/{id}                 # Delete post (soft)
POST   /api/v1/posts/{id}/duplicate       # Duplicate post as template
POST   /api/v1/posts/bulk                 # Bulk operations
```

### Post Scheduling
```
POST   /api/v1/posts/{id}/schedule        # Schedule post for publication
PUT    /api/v1/posts/{id}/schedule        # Update schedule
DELETE /api/v1/posts/{id}/schedule        # Cancel scheduled publication
GET    /api/v1/posts/scheduled            # Get scheduled posts
POST   /api/v1/posts/schedule/optimal     # Get optimal posting times
```

### Media Management
```
POST   /api/v1/media/upload               # Upload media files
GET    /api/v1/media                      # List media library
GET    /api/v1/media/{id}                 # Get media details
PUT    /api/v1/media/{id}                 # Update media metadata
DELETE /api/v1/media/{id}                 # Delete media
POST   /api/v1/media/{id}/edit            # Apply basic edits
```

### Calendar & Planning
```
GET    /api/v1/calendar                   # Get content calendar
GET    /api/v1/calendar/gaps              # Identify content gaps
POST   /api/v1/calendar/reschedule        # Reschedule multiple posts
GET    /api/v1/calendar/analytics         # Calendar performance analytics
```

### Real-time Updates
```
WebSocket: /ws/posts/{user_id}            # Real-time post updates
GET    /api/v1/posts/{id}/status          # Get current post status
POST   /api/v1/notifications/preferences  # Update notification settings
```

## Database Schema Updates

### Enhanced Post Model
```sql
-- Update posts table with comprehensive fields
ALTER TABLE posts ADD COLUMN IF NOT EXISTS post_version INTEGER DEFAULT 1;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS template_name VARCHAR(255);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS tags TEXT[];
ALTER TABLE posts ADD COLUMN IF NOT EXISTS metadata JSONB;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS scheduled_for TIMESTAMP;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS optimal_time_score DECIMAL(3,2);

-- Create version history table
CREATE TABLE post_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    
    -- Versioned content
    caption TEXT,
    hashtags TEXT[],
    media_urls TEXT[],
    metadata JSONB,
    
    -- Version metadata
    changed_by UUID REFERENCES users(id),
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(post_id, version_number)
);

-- Indexes for performance
CREATE INDEX idx_post_versions_post_id ON post_versions(post_id);
CREATE INDEX idx_posts_scheduled_for ON posts(scheduled_for) 
  WHERE scheduled_for IS NOT NULL;
CREATE INDEX idx_posts_tags ON posts USING GIN(tags);
CREATE INDEX idx_posts_deleted_at ON posts(deleted_at) 
  WHERE deleted_at IS NULL;
```

### Media Management
```sql
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- File information
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL, -- 'image', 'video'
    mime_type VARCHAR(100) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    
    -- Media properties
    width INTEGER,
    height INTEGER,
    duration_seconds DECIMAL(8,2), -- For videos
    
    -- Storage information
    storage_url TEXT NOT NULL,
    cdn_url TEXT,
    thumbnail_url TEXT,
    
    -- Organization
    tags TEXT[],
    description TEXT,
    alt_text TEXT,
    
    -- Usage tracking
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for media queries
CREATE INDEX idx_media_files_user_id ON media_files(user_id);
CREATE INDEX idx_media_files_type ON media_files(file_type);
CREATE INDEX idx_media_files_tags ON media_files USING GIN(tags);
CREATE INDEX idx_media_files_created_at ON media_files(created_at);
```

### Scheduling Infrastructure
```sql
CREATE TABLE post_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Scheduling details
    scheduled_time TIMESTAMP NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    optimal_score DECIMAL(3,2),
    
    -- Execution tracking
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'executing', 'completed', 'failed'
    execution_attempts INTEGER DEFAULT 0,
    last_attempt_at TIMESTAMP,
    next_retry_at TIMESTAMP,
    
    -- Results
    published_at TIMESTAMP,
    error_message TEXT,
    instagram_post_id VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(post_id)
);

-- Indexes for scheduling queries
CREATE INDEX idx_post_schedules_scheduled_time ON post_schedules(scheduled_time);
CREATE INDEX idx_post_schedules_status ON post_schedules(status);
CREATE INDEX idx_post_schedules_user_id ON post_schedules(user_id);
CREATE INDEX idx_post_schedules_next_retry ON post_schedules(next_retry_at) 
  WHERE next_retry_at IS NOT NULL;
```

### Real-time Notifications
```sql
CREATE TABLE post_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    
    -- Notification details
    notification_type VARCHAR(50) NOT NULL, -- 'status_change', 'performance_milestone', 'schedule_reminder'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- Delivery tracking
    delivered_at TIMESTAMP,
    read_at TIMESTAMP,
    delivery_method VARCHAR(50), -- 'websocket', 'email', 'push'
    
    -- Metadata
    metadata JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for notification queries
CREATE INDEX idx_notifications_user_id ON post_notifications(user_id);
CREATE INDEX idx_notifications_created_at ON post_notifications(created_at);
CREATE INDEX idx_notifications_read_at ON post_notifications(read_at) 
  WHERE read_at IS NULL;
```

## Implementation Details

### Post Scheduling System
```python
class PostSchedulingService:
    def __init__(self, celery_app: Celery, db: Session):
        self.celery = celery_app
        self.db = db
    
    async def schedule_post(
        self,
        post_id: str,
        scheduled_time: datetime,
        timezone: str,
        user_id: str
    ) -> PostScheduleResponse:
        """Schedule a post for future publication."""
        
        # Convert to UTC and validate timing
        utc_time = self._convert_to_utc(scheduled_time, timezone)
        await self._validate_schedule_time(utc_time)
        
        # Check for conflicts
        conflicts = await self._check_schedule_conflicts(user_id, utc_time)
        if conflicts:
            return PostScheduleResponse(
                success=False,
                conflicts=conflicts,
                suggested_times=await self._suggest_alternative_times(utc_time)
            )
        
        # Calculate optimal timing score
        optimal_score = await self._calculate_optimal_score(user_id, utc_time)
        
        # Create schedule record
        schedule = PostSchedule(
            post_id=post_id,
            user_id=user_id,
            scheduled_time=utc_time,
            timezone=timezone,
            optimal_score=optimal_score
        )
        self.db.add(schedule)
        self.db.commit()
        
        # Schedule Celery task
        task = publish_scheduled_post.apply_async(
            args=[post_id],
            eta=utc_time,
            task_id=f"post_{post_id}_{int(utc_time.timestamp())}"
        )
        
        return PostScheduleResponse(
            success=True,
            schedule_id=schedule.id,
            task_id=task.id,
            optimal_score=optimal_score
        )
    
    async def _calculate_optimal_score(self, user_id: str, scheduled_time: datetime) -> float:
        """Calculate optimal timing score based on audience analytics."""
        
        # Get user's historical performance data
        performance_data = await self._get_performance_history(user_id)
        
        # Analyze day of week and time patterns
        weekday_score = self._analyze_weekday_performance(
            performance_data, scheduled_time.weekday()
        )
        hour_score = self._analyze_hourly_performance(
            performance_data, scheduled_time.hour
        )
        
        # Consider Instagram algorithm factors
        algorithm_score = self._calculate_algorithm_factors(scheduled_time)
        
        # Weighted combination
        return (weekday_score * 0.4 + hour_score * 0.4 + algorithm_score * 0.2)
```

### Media Processing Pipeline
```python
class MediaProcessingService:
    def __init__(self, storage_service: StorageService):
        self.storage = storage_service
        self.image_processor = ImageProcessor()
        self.video_processor = VideoProcessor()
    
    async def process_upload(
        self,
        file: UploadFile,
        user_id: str,
        optimization_level: str = "standard"
    ) -> MediaFileResponse:
        """Process uploaded media file for Instagram optimization."""
        
        # Validate file type and size
        await self._validate_file(file)
        
        # Determine processing path
        if file.content_type.startswith('image/'):
            return await self._process_image(file, user_id, optimization_level)
        elif file.content_type.startswith('video/'):
            return await self._process_video(file, user_id, optimization_level)
        else:
            raise UnsupportedMediaTypeError(f"Unsupported file type: {file.content_type}")
    
    async def _process_image(
        self,
        file: UploadFile,
        user_id: str,
        optimization_level: str
    ) -> MediaFileResponse:
        """Process and optimize image for Instagram."""
        
        # Load image
        image = await self.image_processor.load_image(file)
        
        # Get image properties
        width, height = image.size
        file_size = len(await file.read())
        await file.seek(0)  # Reset file pointer
        
        # Apply Instagram optimization
        optimized_image = await self.image_processor.optimize_for_instagram(
            image, optimization_level
        )
        
        # Generate multiple sizes
        thumbnail = await self.image_processor.generate_thumbnail(optimized_image)
        
        # Store files
        storage_url = await self.storage.store_file(
            optimized_image, f"media/{user_id}/{uuid4()}.jpg"
        )
        thumbnail_url = await self.storage.store_file(
            thumbnail, f"thumbs/{user_id}/{uuid4()}.jpg"
        )
        
        # Save to database
        media_file = MediaFile(
            user_id=user_id,
            filename=f"{uuid4()}.jpg",
            original_filename=file.filename,
            file_type="image",
            mime_type="image/jpeg",
            file_size_bytes=len(optimized_image),
            width=optimized_image.width,
            height=optimized_image.height,
            storage_url=storage_url,
            thumbnail_url=thumbnail_url
        )
        
        return MediaFileResponse.from_orm(media_file)
```

### Real-time Status Updates
```python
class PostStatusService:
    def __init__(self, websocket_manager: WebSocketManager, db: Session):
        self.websocket = websocket_manager
        self.db = db
    
    async def update_post_status(
        self,
        post_id: str,
        status: PostStatus,
        metadata: dict = None
    ):
        """Update post status and notify connected clients."""
        
        # Update post in database
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise PostNotFoundError(f"Post {post_id} not found")
        
        previous_status = post.status
        post.status = status
        post.updated_at = datetime.utcnow()
        
        if metadata:
            post.metadata = {**(post.metadata or {}), **metadata}
        
        self.db.commit()
        
        # Create notification
        notification = await self._create_status_notification(
            post, previous_status, status
        )
        
        # Send real-time update
        update_message = {
            "type": "post_status_update",
            "post_id": post_id,
            "status": status,
            "previous_status": previous_status,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata
        }
        
        await self.websocket.send_to_user(post.user_id, update_message)
        
        # Send push notification if significant status change
        if self._is_significant_status_change(previous_status, status):
            await self._send_push_notification(post.user_id, notification)
    
    async def track_publishing_progress(
        self,
        post_id: str,
        progress_percentage: int,
        current_step: str
    ):
        """Track and broadcast publishing progress."""
        
        progress_message = {
            "type": "publishing_progress",
            "post_id": post_id,
            "progress": progress_percentage,
            "current_step": current_step,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Get post to find user_id
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if post:
            await self.websocket.send_to_user(post.user_id, progress_message)
```

### Content Calendar API
```python
class ContentCalendarService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_calendar_data(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
        view_type: str = "month"
    ) -> CalendarResponse:
        """Get organized calendar data for date range."""
        
        # Query posts in date range
        posts = self.db.query(Post).filter(
            Post.user_id == user_id,
            Post.scheduled_for >= start_date,
            Post.scheduled_for <= end_date,
            Post.deleted_at.is_(None)
        ).order_by(Post.scheduled_for).all()
        
        # Group by date
        calendar_data = self._group_posts_by_date(posts, view_type)
        
        # Add gap analysis
        gaps = await self._analyze_content_gaps(user_id, start_date, end_date)
        
        # Calculate content mix
        content_mix = self._analyze_content_mix(posts)
        
        # Get performance predictions
        predictions = await self._predict_performance(posts)
        
        return CalendarResponse(
            calendar_data=calendar_data,
            content_gaps=gaps,
            content_mix=content_mix,
            performance_predictions=predictions,
            total_posts=len(posts)
        )
    
    async def _analyze_content_gaps(
        self,
        user_id: str,
        start_date: date,
        end_date: date
    ) -> List[ContentGap]:
        """Identify gaps in content schedule."""
        
        # Get user's typical posting frequency
        posting_frequency = await self._get_posting_frequency(user_id)
        
        gaps = []
        current_date = start_date
        
        while current_date <= end_date:
            # Check if date has scheduled posts
            posts_on_date = self.db.query(Post).filter(
                Post.user_id == user_id,
                func.date(Post.scheduled_for) == current_date,
                Post.deleted_at.is_(None)
            ).count()
            
            # Identify gap if posts below frequency target
            if posts_on_date < posting_frequency:
                optimal_times = await self._get_optimal_times(user_id, current_date)
                gaps.append(ContentGap(
                    date=current_date,
                    missing_posts=posting_frequency - posts_on_date,
                    suggested_times=optimal_times,
                    urgency_score=self._calculate_gap_urgency(current_date)
                ))
            
            current_date += timedelta(days=1)
        
        return gaps
```

## Testing Strategy

### Post Management Testing
```python
class TestPostManagement:
    async def test_post_creation_with_validation(self, client, authenticated_user):
        """Test comprehensive post creation with validation."""
        post_data = {
            "caption": "Test caption for home decor post",
            "hashtags": ["#homeDecor", "#modern", "#style"],
            "media_urls": ["https://example.com/image.jpg"],
            "post_type": "photo",
            "tags": ["furniture", "modern"]
        }
        
        response = await client.post("/api/v1/posts", json=post_data)
        assert response.status_code == 201
        
        post = response.json()
        assert post["caption"] == post_data["caption"]
        assert post["hashtags"] == post_data["hashtags"]
        assert post["version"] == 1
    
    async def test_post_scheduling_optimal_timing(self, client, authenticated_user):
        """Test post scheduling with optimal timing suggestions."""
        # Create a post first
        post_response = await client.post("/api/v1/posts", json={
            "caption": "Scheduled post",
            "media_urls": ["https://example.com/image.jpg"]
        })
        post_id = post_response.json()["id"]
        
        # Schedule the post
        schedule_data = {
            "scheduled_time": "2024-02-15T14:00:00",
            "timezone": "America/New_York"
        }
        
        response = await client.post(
            f"/api/v1/posts/{post_id}/schedule",
            json=schedule_data
        )
        
        assert response.status_code == 200
        schedule = response.json()
        assert "optimal_score" in schedule
        assert schedule["optimal_score"] >= 0.0
    
    async def test_media_upload_and_processing(self, client, authenticated_user):
        """Test media upload with automatic processing."""
        # Create test image file
        test_image = create_test_image(1080, 1080, "JPEG")
        
        files = {"file": ("test.jpg", test_image, "image/jpeg")}
        response = await client.post("/api/v1/media/upload", files=files)
        
        assert response.status_code == 201
        media = response.json()
        assert media["width"] == 1080
        assert media["height"] == 1080
        assert "cdn_url" in media
        assert "thumbnail_url" in media
```

### Real-time Testing
```python
class TestRealTimeFeatures:
    async def test_websocket_post_updates(self, websocket_client, authenticated_user):
        """Test real-time post status updates via WebSocket."""
        # Connect to WebSocket
        websocket = await websocket_client.websocket_connect(
            f"/ws/posts/{authenticated_user.id}"
        )
        
        # Create and schedule a post
        post_data = {"caption": "Test post", "media_urls": ["test.jpg"]}
        post_response = await websocket_client.post("/api/v1/posts", json=post_data)
        post_id = post_response.json()["id"]
        
        # Schedule the post for immediate publishing
        await websocket_client.post(f"/api/v1/posts/{post_id}/schedule", json={
            "scheduled_time": datetime.utcnow().isoformat()
        })
        
        # Wait for status update via WebSocket
        message = await websocket.receive_json()
        assert message["type"] == "post_status_update"
        assert message["post_id"] == post_id
        assert message["status"] in ["publishing", "published"]
    
    async def test_publishing_progress_tracking(self, websocket_client, authenticated_user):
        """Test publishing progress updates."""
        websocket = await websocket_client.websocket_connect(
            f"/ws/posts/{authenticated_user.id}"
        )
        
        # Trigger a post publication
        # ... trigger publication ...
        
        # Expect progress updates
        progress_messages = []
        for _ in range(3):  # Expect multiple progress updates
            message = await websocket.receive_json()
            if message["type"] == "publishing_progress":
                progress_messages.append(message)
        
        assert len(progress_messages) > 0
        assert all(0 <= msg["progress"] <= 100 for msg in progress_messages)
```

### Performance Testing
```python
class TestPerformance:
    async def test_bulk_operations_performance(self, client, authenticated_user):
        """Test performance of bulk post operations."""
        # Create 50 posts for bulk testing
        post_ids = []
        for i in range(50):
            response = await client.post("/api/v1/posts", json={
                "caption": f"Bulk test post {i}",
                "media_urls": [f"test{i}.jpg"]
            })
            post_ids.append(response.json()["id"])
        
        # Test bulk scheduling
        start_time = time.time()
        bulk_data = {
            "post_ids": post_ids,
            "operation": "schedule",
            "parameters": {
                "start_time": "2024-02-15T09:00:00",
                "interval_minutes": 60
            }
        }
        
        response = await client.post("/api/v1/posts/bulk", json=bulk_data)
        execution_time = time.time() - start_time
        
        assert response.status_code == 200
        assert execution_time < 5.0  # Should complete within 5 seconds
    
    async def test_calendar_data_performance(self, client, authenticated_user):
        """Test calendar data retrieval performance with large datasets."""
        # Create 100 posts across 3 months
        for i in range(100):
            await client.post("/api/v1/posts", json={
                "caption": f"Calendar test post {i}",
                "scheduled_for": (datetime.utcnow() + timedelta(days=i//10)).isoformat()
            })
        
        # Test calendar retrieval
        start_time = time.time()
        response = await client.get("/api/v1/calendar", params={
            "start_date": "2024-01-01",
            "end_date": "2024-03-31",
            "view_type": "month"
        })
        execution_time = time.time() - start_time
        
        assert response.status_code == 200
        assert execution_time < 2.0  # Should complete within 2 seconds
        
        calendar_data = response.json()
        assert "calendar_data" in calendar_data
        assert "content_gaps" in calendar_data
```

## Performance Benchmarks

### API Response Time Targets
- **Post CRUD Operations**: <300ms for single operations, <2s for bulk (50 items)
- **Scheduling Operations**: <500ms for single post, <5s for bulk scheduling
- **Media Upload**: <10s for image processing, <60s for video processing
- **Calendar Data**: <2s for 3-month view with 100+ posts
- **Real-time Updates**: <100ms latency for WebSocket messages

### Scalability Targets
- **Concurrent Users**: Support 100+ concurrent users without degradation
- **Post Volume**: Handle 10,000+ posts per user without performance issues
- **Media Storage**: Efficiently serve media files via CDN with <200ms global latency
- **Scheduling Load**: Process 1,000+ scheduled posts per hour reliably

## Risk Mitigation

### Technical Risks
1. **Scheduling Reliability**
   - *Risk*: Scheduled posts failing to publish at correct time
   - *Mitigation*: Robust retry logic, monitoring, backup scheduling system

2. **Media Processing Performance**
   - *Risk*: Large files causing timeouts or memory issues
   - *Mitigation*: Async processing, size limits, progress tracking

3. **Real-time System Scalability**
   - *Risk*: WebSocket connections overwhelming server
   - *Mitigation*: Connection pooling, message queuing, horizontal scaling

### Business Risks
1. **Content Loss**
   - *Risk*: Users losing post content due to system failures
   - *Mitigation*: Auto-save, version history, comprehensive backups

2. **Scheduling Conflicts**
   - *Risk*: Double-posting or missed publications
   - *Mitigation*: Conflict detection, user notifications, manual override options

## Definition of Done

### Functionality
- [ ] Complete CRUD operations for posts with validation and error handling
- [ ] Reliable post scheduling with optimal timing suggestions
- [ ] Media upload and processing with Instagram optimization
- [ ] Real-time status updates via WebSocket connections
- [ ] Content calendar with drag-and-drop scheduling interface

### Performance
- [ ] API endpoints meet response time benchmarks
- [ ] Bulk operations handle 50+ items efficiently
- [ ] Media processing completes within time limits
- [ ] Real-time updates have <100ms latency
- [ ] System supports 100+ concurrent users

### Quality
- [ ] 90%+ test coverage for all post management features
- [ ] Integration tests cover complete workflows
- [ ] Performance tests validate scalability requirements
- [ ] Error handling comprehensive for all failure scenarios

### User Experience
- [ ] Intuitive post creation and editing workflow
- [ ] Clear scheduling interface with optimal timing guidance
- [ ] Responsive media upload with progress indicators
- [ ] Real-time feedback for all user actions

## Sprint Review & Retrospective

### Demo Checklist
- [ ] Create, edit, and delete posts with full workflow
- [ ] Schedule posts with optimal timing suggestions
- [ ] Upload and process multiple media types
- [ ] Show real-time status updates via WebSocket
- [ ] Navigate content calendar with drag-and-drop scheduling

### Key Metrics to Review
- Post creation and scheduling success rates
- Media processing performance and quality
- Real-time update delivery reliability
- User workflow completion rates
- System performance under load

## Handoff to Sprint 5

### Deliverables for Next Sprint
- [ ] Complete post management system ready for campaign integration
- [ ] Scheduling infrastructure prepared for automated campaign posting
- [ ] Media management system ready for campaign content
- [ ] Real-time updates infrastructure available for campaign monitoring

### Next Sprint Preparation
- [ ] Campaign automation workflow design
- [ ] Multi-post campaign coordination planning
- [ ] Campaign performance tracking research
- [ ] Sprint 5 detailed task planning and story estimation