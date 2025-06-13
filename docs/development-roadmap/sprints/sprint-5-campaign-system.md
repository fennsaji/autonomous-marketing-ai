# Sprint 5: Campaign Management System
**Duration**: Weeks 9-10 | **Focus**: Campaign Automation & Multi-Post Orchestration

## Sprint Goals

### Primary Objectives
- ✅ Build comprehensive campaign creation and management system
- ✅ Implement automated content generation for campaign themes
- ✅ Create multi-post campaign orchestration and scheduling
- ✅ Establish campaign performance tracking and optimization
- ✅ Develop campaign templates and automation workflows

### Success Criteria
- [ ] Users can create campaigns with automated content generation
- [ ] Campaigns automatically generate and schedule multiple posts
- [ ] Campaign performance tracked with ROI calculation and insights
- [ ] Campaign templates enable quick setup for common scenarios
- [ ] Campaign optimization suggestions improve performance over time

## Epic Breakdown

### Epic 1: Campaign Core Management
**Story Points**: 12 | **Priority**: Critical

#### User Stories
1. **CAMP-001**: As a user, I can create marketing campaigns with strategic goals
   - Campaign setup with objectives, duration, and target metrics
   - Content theme selection and brand voice configuration
   - Budget allocation and cost tracking
   - Campaign timeline and milestone planning
   - **Acceptance Criteria**:
     - POST /campaigns creates campaign with validation
     - Support for multiple campaign objectives (awareness, engagement, sales)
     - Budget tracking and alerts for overspend protection
     - Timeline visualization with key milestones

2. **CAMP-002**: As a user, I can manage campaign lifecycle and settings
   - Campaign activation, pause, and termination controls
   - Real-time campaign modification and optimization
   - Campaign duplication and template creation
   - Performance monitoring and adjustment recommendations
   - **Acceptance Criteria**:
     - Campaign status controls work reliably
     - Live campaigns can be modified without disruption
     - Template creation preserves successful campaign patterns
     - Performance dashboards provide actionable insights

3. **CAMP-003**: As a user, I can organize campaigns with categorization
   - Campaign folders and organization system
   - Tagging and labeling for easy discovery
   - Campaign search and filtering capabilities
   - Archive system for completed campaigns
   - **Acceptance Criteria**:
     - Campaigns can be organized in hierarchical folders
     - Advanced search supports multiple filter criteria
     - Archived campaigns retain full historical data
     - Export capabilities for campaign reporting

#### Technical Tasks
- [ ] Design comprehensive campaign data model
- [ ] Implement campaign CRUD operations with validation
- [ ] Build campaign lifecycle management system
- [ ] Create campaign organization and search functionality
- [ ] Add campaign template system with inheritance

### Epic 2: Automated Content Generation for Campaigns
**Story Points**: 14 | **Priority**: Critical

#### User Stories
1. **CAMP-004**: As a user, I can configure automated content generation
   - Content theme specification and variation parameters
   - Automated posting frequency and timing optimization
   - Brand voice consistency across campaign content
   - Content mix optimization (images, videos, carousels)
   - **Acceptance Criteria**:
     - Campaign themes generate diverse, relevant content
     - Posting frequency adapts to optimal engagement times
     - Brand voice remains consistent across all generated content
     - Content mix follows proven engagement patterns

2. **CAMP-005**: As a user, I can customize campaign content automation
   - Custom content templates and prompt engineering
   - Hashtag strategy and distribution optimization
   - Visual style consistency and brand guideline adherence
   - Content quality control and approval workflows
   - **Acceptance Criteria**:
     - Custom templates produce high-quality, on-brand content
     - Hashtag distribution prevents over-saturation
     - Visual content maintains consistent brand aesthetic
     - Approval workflows prevent inappropriate content publication

3. **CAMP-006**: As a system, I can optimize campaign content automatically
   - Performance-based content adaptation and improvement
   - A/B testing for campaign content variations
   - Trend incorporation and timely content updates
   - Cost optimization for AI-generated content
   - **Acceptance Criteria**:
     - Content adapts based on real-time performance data
     - A/B tests provide statistically significant insights
     - Trending topics incorporated without brand compromise
     - AI costs remain within campaign budget constraints

#### Technical Tasks
- [ ] Build campaign content generation pipeline
- [ ] Implement AI prompt templates for campaign themes
- [ ] Create content variation and A/B testing system
- [ ] Add performance-based content optimization
- [ ] Integrate cost tracking and budget management

### Epic 3: Multi-Post Campaign Orchestration
**Story Points**: 10 | **Priority**: High

#### User Stories
1. **CAMP-007**: As a user, I can coordinate multiple posts within campaigns
   - Sequential post scheduling with story arc development
   - Cross-post promotion and engagement strategies
   - Campaign narrative consistency and message coordination
   - Multi-platform content adaptation and timing
   - **Acceptance Criteria**:
     - Posts within campaigns follow coherent narrative progression
     - Cross-references between posts drive engagement
     - Message consistency maintained across campaign duration
     - Content adapted for optimal platform-specific performance

2. **CAMP-008**: As a user, I can manage campaign posting schedules
   - Intelligent spacing between campaign posts
   - Conflict resolution with organic content
   - Holiday and event-aware scheduling adjustments
   - Real-time schedule optimization based on performance
   - **Acceptance Criteria**:
     - Campaign posts optimally spaced for maximum impact
     - Scheduling conflicts resolved automatically with user notification
     - Holiday schedules adjust automatically with user approval
     - Performance data drives real-time schedule optimization

#### Technical Tasks
- [ ] Design multi-post coordination algorithms
- [ ] Implement intelligent post spacing and timing
- [ ] Build campaign narrative progression system
- [ ] Create conflict resolution and optimization engine
- [ ] Add holiday and event-aware scheduling

### Epic 4: Campaign Performance & Analytics
**Story Points**: 8 | **Priority**: High

#### User Stories
1. **CAMP-009**: As a user, I can track campaign performance comprehensively
   - Real-time campaign metrics and KPI monitoring
   - ROI calculation with cost attribution and revenue tracking
   - Audience engagement analysis and demographic insights
   - Competitive performance benchmarking
   - **Acceptance Criteria**:
     - Campaign dashboard provides real-time performance overview
     - ROI calculations accurate and include all cost factors
     - Audience insights show campaign reach and engagement patterns
     - Benchmarking compares performance against industry standards

2. **CAMP-010**: As a user, I can optimize campaigns based on insights
   - Performance alerts and optimization recommendations
   - Automated budget reallocation and bid adjustments
   - Content performance analysis and improvement suggestions
   - Campaign extension or termination recommendations
   - **Acceptance Criteria**:
     - Alerts trigger for significant performance changes
     - Budget optimizations improve overall campaign efficiency
     - Content recommendations based on top-performing variations
     - Campaign lifecycle recommendations maximize ROI

#### Technical Tasks
- [ ] Build comprehensive campaign analytics system
- [ ] Implement ROI calculation and attribution modeling
- [ ] Create performance alerting and notification system
- [ ] Add optimization recommendation engine
- [ ] Build competitive benchmarking capabilities

### Epic 5: Campaign Templates & Automation
**Story Points**: 6 | **Priority**: Medium

#### User Stories
1. **CAMP-011**: As a user, I can use pre-built campaign templates
   - Industry-specific campaign templates (furniture, decor, lifestyle)
   - Seasonal campaign templates with timely content
   - Goal-oriented templates (product launch, brand awareness, sales)
   - Customizable template parameters and personalization
   - **Acceptance Criteria**:
     - Templates cover common home decor marketing scenarios
     - Seasonal templates align with home decor industry trends
     - Goal-specific templates optimize for different objectives
     - Template customization maintains proven structure while allowing personalization

2. **CAMP-012**: As a user, I can create and share custom templates
   - Template creation from successful campaigns
   - Template sharing and collaboration features
   - Template performance tracking and recommendations
   - Version control and template evolution tracking
   - **Acceptance Criteria**:
     - Successful campaigns can be templated for reuse
     - Template sharing enables team collaboration
     - Template performance data guides selection decisions
     - Version control tracks template improvements over time

#### Technical Tasks
- [ ] Design campaign template system architecture
- [ ] Create library of home decor industry templates
- [ ] Implement template customization and parameterization
- [ ] Build template sharing and collaboration features
- [ ] Add template performance tracking and recommendations

## Detailed Task Breakdown

### Week 1 Tasks (Days 1-5)

#### Day 1: Campaign Data Foundation
- [ ] **MODEL-001**: Design comprehensive campaign database schema
- [ ] **MODEL-002**: Create campaign model with objectives and metrics
- [ ] **MODEL-003**: Implement campaign-post relationship management
- [ ] **MODEL-004**: Add campaign budget and cost tracking tables
- [ ] **MODEL-005**: Create campaign template and inheritance system

#### Day 2-3: Campaign Core Operations
- [ ] **CRUD-001**: Implement campaign creation with validation
- [ ] **CRUD-002**: Build campaign update and modification endpoints
- [ ] **CRUD-003**: Add campaign lifecycle management (activate/pause/stop)
- [ ] **CRUD-004**: Create campaign organization and folder system
- [ ] **CRUD-005**: Implement campaign search and filtering

#### Day 4-5: Content Generation Pipeline
- [ ] **CONTENT-001**: Build campaign content generation service
- [ ] **CONTENT-002**: Create campaign-specific AI prompt templates
- [ ] **CONTENT-003**: Implement content theme variation algorithms
- [ ] **CONTENT-004**: Add brand voice consistency validation
- [ ] **CONTENT-005**: Create content quality scoring for campaigns

### Week 2 Tasks (Days 6-10)

#### Day 1-2: Multi-Post Orchestration
- [ ] **ORCHESTRATION-001**: Design multi-post coordination algorithms
- [ ] **ORCHESTRATION-002**: Implement intelligent post spacing logic
- [ ] **ORCHESTRATION-003**: Build campaign narrative progression system
- [ ] **ORCHESTRATION-004**: Create conflict resolution engine
- [ ] **ORCHESTRATION-005**: Add cross-post promotion features

#### Day 3: Performance & Analytics
- [ ] **ANALYTICS-001**: Build campaign performance tracking system
- [ ] **ANALYTICS-002**: Implement ROI calculation and attribution
- [ ] **ANALYTICS-003**: Create campaign alert and notification system
- [ ] **ANALYTICS-004**: Add optimization recommendation engine
- [ ] **ANALYTICS-005**: Build campaign comparison and benchmarking

#### Day 4-5: Templates & Integration
- [ ] **TEMPLATE-001**: Create campaign template library
- [ ] **TEMPLATE-002**: Implement template customization system
- [ ] **TEMPLATE-003**: Build template sharing and collaboration
- [ ] **TEMPLATE-004**: Integrate campaigns with existing post management
- [ ] **TEMPLATE-005**: Create campaign automation workflows

## API Endpoints to Deliver

### Campaign Management
```
GET    /api/v1/campaigns                   # List campaigns with filters
POST   /api/v1/campaigns                   # Create new campaign
GET    /api/v1/campaigns/{id}              # Get specific campaign
PUT    /api/v1/campaigns/{id}              # Update campaign
DELETE /api/v1/campaigns/{id}              # Delete campaign
POST   /api/v1/campaigns/{id}/duplicate    # Duplicate campaign
```

### Campaign Lifecycle
```
POST   /api/v1/campaigns/{id}/activate     # Activate campaign
POST   /api/v1/campaigns/{id}/pause        # Pause campaign
POST   /api/v1/campaigns/{id}/stop         # Stop campaign
POST   /api/v1/campaigns/{id}/optimize     # Optimize campaign settings
```

### Campaign Content
```
POST   /api/v1/campaigns/{id}/generate     # Generate campaign content
GET    /api/v1/campaigns/{id}/posts        # Get campaign posts
POST   /api/v1/campaigns/{id}/posts/schedule # Schedule campaign posts
GET    /api/v1/campaigns/{id}/content/preview # Preview generated content
```

### Campaign Analytics
```
GET    /api/v1/campaigns/{id}/analytics    # Campaign performance data
GET    /api/v1/campaigns/{id}/roi          # ROI calculation and breakdown
GET    /api/v1/campaigns/{id}/insights     # Performance insights and recommendations
POST   /api/v1/campaigns/{id}/report       # Generate campaign report
```

### Campaign Templates
```
GET    /api/v1/campaign-templates          # List available templates
GET    /api/v1/campaign-templates/{id}     # Get template details
POST   /api/v1/campaign-templates          # Create custom template
POST   /api/v1/campaigns/from-template/{id} # Create campaign from template
```

## Database Schema Updates

### Campaign Core Schema
```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Campaign basic info
    name VARCHAR(255) NOT NULL,
    description TEXT,
    objective VARCHAR(50) NOT NULL, -- 'awareness', 'engagement', 'traffic', 'sales'
    
    -- Campaign timeline
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- Campaign status
    status VARCHAR(20) DEFAULT 'draft', -- 'draft', 'active', 'paused', 'completed', 'cancelled'
    is_active BOOLEAN DEFAULT false,
    
    -- Content configuration
    content_themes JSONB, -- Array of themes like ["modern_living", "cozy_bedroom"]
    brand_voice VARCHAR(50) DEFAULT 'professional',
    posts_per_day INTEGER DEFAULT 1,
    content_mix JSONB, -- Distribution like {"photo": 60, "video": 20, "carousel": 20}
    
    -- Budget and costs
    total_budget_cents INTEGER,
    spent_budget_cents INTEGER DEFAULT 0,
    daily_budget_cents INTEGER,
    
    -- Performance targets
    target_reach INTEGER,
    target_engagement_rate DECIMAL(5,2),
    target_conversions INTEGER,
    
    -- Automation settings
    auto_generate_content BOOLEAN DEFAULT true,
    auto_optimize_timing BOOLEAN DEFAULT true,
    auto_adjust_budget BOOLEAN DEFAULT false,
    
    -- Organization
    folder_path TEXT,
    tags TEXT[],
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_dates ON campaigns(start_date, end_date);
CREATE INDEX idx_campaigns_active ON campaigns(is_active) WHERE is_active = true;
```

### Campaign Posts Relationship
```sql
-- Add campaign relationship to posts table
ALTER TABLE posts ADD COLUMN IF NOT EXISTS campaign_id UUID REFERENCES campaigns(id) ON DELETE SET NULL;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS campaign_sequence INTEGER;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS campaign_role VARCHAR(50); -- 'intro', 'content', 'promotion', 'conclusion'

-- Create index for campaign queries
CREATE INDEX idx_posts_campaign_id ON posts(campaign_id);
CREATE INDEX idx_posts_campaign_sequence ON posts(campaign_id, campaign_sequence);
```

### Campaign Performance Tracking
```sql
CREATE TABLE campaign_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    
    -- Time period
    date DATE NOT NULL,
    hour_bucket INTEGER, -- 0-23 for hourly tracking
    
    -- Content metrics
    posts_published INTEGER DEFAULT 0,
    content_generation_cost_cents INTEGER DEFAULT 0,
    
    -- Engagement metrics
    total_likes INTEGER DEFAULT 0,
    total_comments INTEGER DEFAULT 0,
    total_shares INTEGER DEFAULT 0,
    total_saves INTEGER DEFAULT 0,
    total_reach INTEGER DEFAULT 0,
    total_impressions INTEGER DEFAULT 0,
    
    -- Business metrics
    website_clicks INTEGER DEFAULT 0,
    profile_visits INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue_cents INTEGER DEFAULT 0,
    
    -- Calculated metrics
    engagement_rate DECIMAL(5,2),
    cost_per_engagement_cents INTEGER,
    cost_per_conversion_cents INTEGER,
    roas DECIMAL(8,2), -- Return on Ad Spend
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(campaign_id, date, hour_bucket)
);

-- Indexes for analytics queries
CREATE INDEX idx_campaign_performance_campaign_date ON campaign_performance(campaign_id, date);
CREATE INDEX idx_campaign_performance_metrics ON campaign_performance(engagement_rate, cost_per_engagement_cents);
```

### Campaign Templates
```sql
CREATE TABLE campaign_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Template metadata
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50), -- 'industry', 'seasonal', 'goal', 'custom'
    subcategory VARCHAR(50), -- 'furniture', 'spring', 'product_launch', etc.
    
    -- Template configuration
    template_config JSONB NOT NULL, -- Full campaign configuration
    customizable_fields JSONB, -- Which fields can be customized
    
    -- Usage and performance
    usage_count INTEGER DEFAULT 0,
    avg_performance_score DECIMAL(3,2),
    success_rate DECIMAL(3,2),
    
    -- Sharing and access
    is_public BOOLEAN DEFAULT false,
    is_verified BOOLEAN DEFAULT false, -- Verified by platform
    
    -- Metadata
    version VARCHAR(10) DEFAULT '1.0',
    tags TEXT[],
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for template queries
CREATE INDEX idx_campaign_templates_category ON campaign_templates(category, subcategory);
CREATE INDEX idx_campaign_templates_public ON campaign_templates(is_public) WHERE is_public = true;
CREATE INDEX idx_campaign_templates_performance ON campaign_templates(avg_performance_score DESC);
```

### Campaign Content Generation Log
```sql
CREATE TABLE campaign_content_generation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    post_id UUID REFERENCES posts(id) ON DELETE SET NULL,
    
    -- Generation details
    generation_type VARCHAR(50), -- 'caption', 'image', 'hashtags', 'complete_post'
    theme_used VARCHAR(100),
    ai_model_used VARCHAR(50),
    
    -- Generation parameters
    generation_params JSONB,
    prompt_used TEXT,
    
    -- Results and quality
    generated_content JSONB,
    quality_score DECIMAL(3,2),
    brand_compliance_score DECIMAL(3,2),
    
    -- Cost and performance
    generation_cost_cents INTEGER,
    tokens_used INTEGER,
    processing_time_ms INTEGER,
    
    -- Usage tracking
    was_used BOOLEAN DEFAULT false,
    user_rating INTEGER, -- 1-5 stars
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for generation analytics
CREATE INDEX idx_campaign_content_campaign_id ON campaign_content_generation(campaign_id);
CREATE INDEX idx_campaign_content_quality ON campaign_content_generation(quality_score);
CREATE INDEX idx_campaign_content_cost ON campaign_content_generation(generation_cost_cents);
```

## Implementation Details

### Campaign Content Generation Pipeline
```python
class CampaignContentService:
    def __init__(self, ai_service: AIService, db: Session):
        self.ai = ai_service
        self.db = db
    
    async def generate_campaign_content(
        self,
        campaign_id: str,
        content_count: int = None,
        preview_only: bool = False
    ) -> CampaignContentResponse:
        """Generate content for entire campaign based on themes and objectives."""
        
        campaign = await self._get_campaign(campaign_id)
        
        # Calculate content requirements
        if not content_count:
            content_count = self._calculate_content_needs(campaign)
        
        # Generate content variations based on themes
        generated_content = []
        
        for theme in campaign.content_themes:
            theme_content = await self._generate_theme_content(
                campaign, theme, content_count // len(campaign.content_themes)
            )
            generated_content.extend(theme_content)
        
        # Optimize content mix and sequencing
        optimized_content = await self._optimize_content_sequence(
            generated_content, campaign
        )
        
        # Create posts if not preview only
        if not preview_only:
            created_posts = await self._create_campaign_posts(
                campaign_id, optimized_content
            )
            await self._schedule_campaign_posts(campaign_id, created_posts)
            
            return CampaignContentResponse(
                campaign_id=campaign_id,
                posts_created=len(created_posts),
                content_preview=optimized_content[:5],  # First 5 for preview
                total_cost_cents=sum(c.generation_cost for c in generated_content)
            )
        
        return CampaignContentResponse(
            campaign_id=campaign_id,
            content_preview=optimized_content,
            estimated_cost_cents=sum(c.estimated_cost for c in generated_content)
        )
    
    async def _generate_theme_content(
        self,
        campaign: Campaign,
        theme: str,
        count: int
    ) -> List[GeneratedContent]:
        """Generate content variations for specific theme."""
        
        content_variations = []
        
        for i in range(count):
            # Generate caption
            caption = await self.ai.generate_caption(
                product_description=f"Defeah {theme} home decor collection",
                tone=campaign.brand_voice,
                style="engaging",
                campaign_context=campaign.objective
            )
            
            # Generate image if required
            image_url = None
            if self._should_generate_image(campaign.content_mix, i):
                image_url = await self.ai.generate_image(
                    prompt=f"Beautiful {theme} home decor setup, Defeah style",
                    style=self._get_visual_style(campaign),
                    quality="hd"
                )
            
            # Generate hashtags
            hashtags = await self.ai.suggest_hashtags(
                content_description=f"{theme} {caption[:100]}",
                niche="home_decor",
                count=15
            )
            
            # Score content quality
            quality_score = await self._score_content_quality(
                caption, image_url, hashtags, campaign
            )
            
            content_variations.append(GeneratedContent(
                theme=theme,
                caption=caption,
                image_url=image_url,
                hashtags=hashtags,
                quality_score=quality_score,
                sequence_position=i
            ))
        
        return content_variations
    
    async def _optimize_content_sequence(
        self,
        content_list: List[GeneratedContent],
        campaign: Campaign
    ) -> List[GeneratedContent]:
        """Optimize content sequencing for maximum campaign impact."""
        
        # Sort by quality score initially
        content_list.sort(key=lambda x: x.quality_score, reverse=True)
        
        # Create campaign narrative flow
        intro_content = [c for c in content_list if self._is_intro_content(c)]
        main_content = [c for c in content_list if self._is_main_content(c)]
        promo_content = [c for c in content_list if self._is_promotional_content(c)]
        conclusion_content = [c for c in content_list if self._is_conclusion_content(c)]
        
        # Sequence optimization based on campaign objectives
        if campaign.objective == "awareness":
            sequence = self._optimize_for_awareness(intro_content, main_content, promo_content)
        elif campaign.objective == "sales":
            sequence = self._optimize_for_sales(intro_content, main_content, promo_content)
        else:
            sequence = self._optimize_for_engagement(intro_content, main_content, promo_content)
        
        # Add campaign roles
        for i, content in enumerate(sequence):
            content.campaign_role = self._determine_content_role(i, len(sequence))
            content.optimal_posting_time = await self._calculate_optimal_time(
                campaign, i, len(sequence)
            )
        
        return sequence
```

### Multi-Post Campaign Orchestration
```python
class CampaignOrchestrationService:
    def __init__(self, scheduler: PostSchedulingService, db: Session):
        self.scheduler = scheduler
        self.db = db
    
    async def orchestrate_campaign(
        self,
        campaign_id: str,
        posts: List[Post]
    ) -> CampaignOrchestrationResponse:
        """Orchestrate multi-post campaign with intelligent timing and sequencing."""
        
        campaign = await self._get_campaign(campaign_id)
        
        # Calculate optimal posting schedule
        posting_schedule = await self._calculate_posting_schedule(campaign, posts)
        
        # Check for conflicts with existing content
        conflicts = await self._check_schedule_conflicts(campaign.user_id, posting_schedule)
        
        if conflicts:
            # Resolve conflicts automatically where possible
            resolved_schedule = await self._resolve_schedule_conflicts(
                posting_schedule, conflicts
            )
            
            # Notify user of changes
            await self._notify_schedule_changes(campaign.user_id, conflicts, resolved_schedule)
            posting_schedule = resolved_schedule
        
        # Schedule all posts
        scheduled_posts = []
        for post, schedule_time in posting_schedule:
            scheduled_post = await self.scheduler.schedule_post(
                post_id=post.id,
                scheduled_time=schedule_time,
                timezone=campaign.timezone,
                user_id=campaign.user_id
            )
            scheduled_posts.append(scheduled_post)
        
        # Set up cross-post promotion
        await self._setup_cross_promotion(posts, posting_schedule)
        
        # Initialize performance tracking
        await self._initialize_campaign_tracking(campaign_id, posts)
        
        return CampaignOrchestrationResponse(
            campaign_id=campaign_id,
            posts_scheduled=len(scheduled_posts),
            schedule_conflicts_resolved=len(conflicts),
            estimated_completion=posting_schedule[-1][1],
            cross_promotion_links=await self._get_promotion_links(posts)
        )
    
    async def _calculate_posting_schedule(
        self,
        campaign: Campaign,
        posts: List[Post]
    ) -> List[Tuple[Post, datetime]]:
        """Calculate optimal posting schedule for campaign."""
        
        # Get user's optimal posting times
        optimal_times = await self._get_user_optimal_times(campaign.user_id)
        
        # Calculate spacing between posts
        campaign_duration = (campaign.end_date - campaign.start_date).days
        posts_per_day = campaign.posts_per_day
        
        if posts_per_day > 1:
            # Multiple posts per day - space throughout optimal hours
            hours_between_posts = 24 // posts_per_day
        else:
            # Single post per day - use best time each day
            hours_between_posts = 24
        
        schedule = []
        current_time = campaign.start_date
        
        for i, post in enumerate(posts):
            # Find next optimal time
            post_time = await self._find_next_optimal_time(
                current_time, optimal_times, campaign.timezone
            )
            
            # Adjust for post role and campaign narrative
            if post.campaign_role == "intro":
                # Intro posts should go at peak engagement times
                post_time = await self._adjust_for_peak_engagement(post_time)
            elif post.campaign_role == "promotion":
                # Promotional posts during high-activity periods
                post_time = await self._adjust_for_high_activity(post_time)
            
            schedule.append((post, post_time))
            
            # Calculate next posting time
            if posts_per_day > 1 and (i + 1) % posts_per_day != 0:
                # Same day, next time slot
                current_time = post_time + timedelta(hours=hours_between_posts)
            else:
                # Next day
                current_time = post_time + timedelta(days=1)
                current_time = current_time.replace(
                    hour=optimal_times[0].hour,
                    minute=optimal_times[0].minute
                )
        
        return schedule
```

### Campaign Performance Analytics
```python
class CampaignAnalyticsService:
    def __init__(self, db: Session, instagram_service: InstagramService):
        self.db = db
        self.instagram = instagram_service
    
    async def calculate_campaign_roi(
        self,
        campaign_id: str,
        include_projections: bool = True
    ) -> CampaignROIResponse:
        """Calculate comprehensive ROI for campaign."""
        
        campaign = await self._get_campaign(campaign_id)
        
        # Get all campaign costs
        total_costs = await self._calculate_total_costs(campaign_id)
        
        # Get campaign performance data
        performance_data = await self._get_campaign_performance(campaign_id)
        
        # Calculate revenue attribution
        attributed_revenue = await self._calculate_attributed_revenue(campaign_id)
        
        # Calculate ROI metrics
        roi_percentage = ((attributed_revenue - total_costs) / total_costs * 100) if total_costs > 0 else 0
        cost_per_engagement = total_costs / performance_data.total_engagements if performance_data.total_engagements > 0 else 0
        cost_per_conversion = total_costs / performance_data.conversions if performance_data.conversions > 0 else 0
        
        # Add projections if campaign is still active
        projections = None
        if include_projections and campaign.status == "active":
            projections = await self._calculate_projections(campaign, performance_data)
        
        return CampaignROIResponse(
            campaign_id=campaign_id,
            total_investment_cents=total_costs,
            attributed_revenue_cents=attributed_revenue,
            roi_percentage=roi_percentage,
            cost_per_engagement_cents=cost_per_engagement,
            cost_per_conversion_cents=cost_per_conversion,
            performance_data=performance_data,
            projections=projections,
            optimization_recommendations=await self._generate_optimization_recommendations(
                campaign, performance_data, roi_percentage
            )
        )
    
    async def _calculate_total_costs(self, campaign_id: str) -> int:
        """Calculate all costs associated with campaign."""
        
        # AI content generation costs
        ai_costs = self.db.query(func.sum(CampaignContentGeneration.generation_cost_cents)).filter(
            CampaignContentGeneration.campaign_id == campaign_id
        ).scalar() or 0
        
        # Estimated time costs (if tracking labor)
        time_costs = await self._calculate_time_costs(campaign_id)
        
        # Tool and platform costs (allocated portion)
        platform_costs = await self._calculate_platform_costs(campaign_id)
        
        return ai_costs + time_costs + platform_costs
    
    async def _generate_optimization_recommendations(
        self,
        campaign: Campaign,
        performance: CampaignPerformance,
        roi: float
    ) -> List[OptimizationRecommendation]:
        """Generate AI-powered optimization recommendations."""
        
        recommendations = []
        
        # Analyze posting timing
        if performance.avg_engagement_rate < 5.0:  # Below average for home decor
            best_times = await self._analyze_best_performing_times(campaign.id)
            recommendations.append(OptimizationRecommendation(
                type="timing",
                priority="high",
                title="Optimize Posting Times",
                description=f"Posts at {best_times} show 25% higher engagement",
                expected_improvement="25% engagement increase",
                implementation_effort="low"
            ))
        
        # Analyze content performance
        top_content = await self._get_top_performing_content(campaign.id)
        if top_content:
            recommendations.append(OptimizationRecommendation(
                type="content",
                priority="medium",
                title="Replicate High-Performing Content",
                description=f"Content with '{top_content.theme}' theme performs 40% better",
                expected_improvement="30-40% engagement increase",
                implementation_effort="medium"
            ))
        
        # Budget optimization
        if roi > 300:  # High ROI suggests we could invest more
            recommendations.append(OptimizationRecommendation(
                type="budget",
                priority="medium",
                title="Increase Campaign Investment",
                description=f"ROI of {roi}% suggests opportunity to scale",
                expected_improvement=f"Potential to double results with 50% budget increase",
                implementation_effort="low"
            ))
        
        return recommendations
```

### Campaign Template System
```python
class CampaignTemplateService:
    def __init__(self, db: Session):
        self.db = db
        self.default_templates = self._load_default_templates()
    
    async def get_recommended_templates(
        self,
        user_id: str,
        objective: str = None,
        industry: str = "home_decor"
    ) -> List[CampaignTemplate]:
        """Get recommended templates based on user profile and objectives."""
        
        # Get user's campaign history for personalization
        user_history = await self._get_user_campaign_history(user_id)
        
        # Filter templates by criteria
        templates = self.db.query(CampaignTemplate).filter(
            CampaignTemplate.is_public == True,
            CampaignTemplate.category.in_(["industry", "goal", "verified"])
        )
        
        if objective:
            templates = templates.filter(
                CampaignTemplate.template_config["objective"].astext == objective
            )
        
        # Score templates based on user fit
        scored_templates = []
        for template in templates.all():
            score = await self._calculate_template_fit_score(template, user_history)
            scored_templates.append((template, score))
        
        # Sort by score and return top recommendations
        scored_templates.sort(key=lambda x: x[1], reverse=True)
        
        return [template for template, score in scored_templates[:10]]
    
    async def create_campaign_from_template(
        self,
        template_id: str,
        user_id: str,
        customizations: dict = None
    ) -> Campaign:
        """Create new campaign from template with optional customizations."""
        
        template = self.db.query(CampaignTemplate).filter(
            CampaignTemplate.id == template_id
        ).first()
        
        if not template:
            raise TemplateNotFoundError(f"Template {template_id} not found")
        
        # Load template configuration
        config = template.template_config.copy()
        
        # Apply customizations
        if customizations:
            config = self._apply_customizations(config, customizations, template.customizable_fields)
        
        # Create campaign from template
        campaign = Campaign(
            user_id=user_id,
            name=config.get("name", f"Campaign from {template.name}"),
            description=config.get("description", template.description),
            objective=config["objective"],
            start_date=config.get("start_date", datetime.utcnow()),
            end_date=config.get("end_date", datetime.utcnow() + timedelta(days=30)),
            content_themes=config["content_themes"],
            brand_voice=config.get("brand_voice", "professional"),
            posts_per_day=config.get("posts_per_day", 1),
            content_mix=config.get("content_mix", {"photo": 70, "video": 30}),
            target_reach=config.get("target_reach"),
            target_engagement_rate=config.get("target_engagement_rate"),
            auto_generate_content=config.get("auto_generate_content", True)
        )
        
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        
        # Update template usage statistics
        template.usage_count += 1
        self.db.commit()
        
        # Generate initial content if auto-generation enabled
        if campaign.auto_generate_content:
            content_service = CampaignContentService(self.ai, self.db)
            await content_service.generate_campaign_content(campaign.id)
        
        return campaign
    
    def _load_default_templates(self) -> List[dict]:
        """Load default campaign templates for home decor industry."""
        
        return [
            {
                "name": "Spring Home Refresh",
                "category": "seasonal",
                "subcategory": "spring",
                "description": "Showcase spring home decor trends and fresh styling ideas",
                "config": {
                    "objective": "awareness",
                    "content_themes": ["spring_colors", "fresh_decor", "seasonal_styling"],
                    "brand_voice": "inspiring",
                    "posts_per_day": 1,
                    "content_mix": {"photo": 60, "video": 20, "carousel": 20},
                    "duration_days": 21,
                    "target_engagement_rate": 8.0
                }
            },
            {
                "name": "Product Launch Campaign",
                "category": "goal",
                "subcategory": "product_launch",
                "description": "Comprehensive product launch with teaser, reveal, and follow-up content",
                "config": {
                    "objective": "sales",
                    "content_themes": ["product_teaser", "product_reveal", "styling_ideas", "customer_reviews"],
                    "brand_voice": "exciting",
                    "posts_per_day": 2,
                    "content_mix": {"photo": 40, "video": 30, "carousel": 30},
                    "duration_days": 14,
                    "target_conversions": 50
                }
            },
            {
                "name": "Room Makeover Series",
                "category": "industry",
                "subcategory": "furniture",
                "description": "Multi-part series showing complete room transformations",
                "config": {
                    "objective": "engagement",
                    "content_themes": ["before_after", "styling_process", "final_reveal", "tips_tricks"],
                    "brand_voice": "educational",
                    "posts_per_day": 1,
                    "content_mix": {"photo": 30, "video": 50, "carousel": 20},
                    "duration_days": 28,
                    "target_engagement_rate": 12.0
                }
            }
        ]
```

## Testing Strategy

### Campaign System Testing
```python
class TestCampaignSystem:
    async def test_campaign_creation_and_lifecycle(self, client, authenticated_user):
        """Test complete campaign creation and lifecycle management."""
        # Create campaign
        campaign_data = {
            "name": "Test Home Decor Campaign",
            "objective": "awareness",
            "start_date": "2024-02-01T09:00:00Z",
            "end_date": "2024-02-28T17:00:00Z",
            "content_themes": ["modern_living", "cozy_bedroom"],
            "posts_per_day": 1,
            "auto_generate_content": True
        }
        
        response = await client.post("/api/v1/campaigns", json=campaign_data)
        assert response.status_code == 201
        
        campaign = response.json()
        campaign_id = campaign["id"]
        
        # Test campaign activation
        activate_response = await client.post(f"/api/v1/campaigns/{campaign_id}/activate")
        assert activate_response.status_code == 200
        
        # Verify content was auto-generated
        posts_response = await client.get(f"/api/v1/campaigns/{campaign_id}/posts")
        assert posts_response.status_code == 200
        posts = posts_response.json()
        assert len(posts) > 0
        
        # Test campaign performance tracking
        analytics_response = await client.get(f"/api/v1/campaigns/{campaign_id}/analytics")
        assert analytics_response.status_code == 200
    
    async def test_campaign_content_generation(self, client, authenticated_user, mock_ai_service):
        """Test automated campaign content generation."""
        # Create campaign
        campaign_response = await client.post("/api/v1/campaigns", json={
            "name": "Content Generation Test",
            "content_themes": ["modern_furniture", "home_styling"],
            "auto_generate_content": False
        })
        campaign_id = campaign_response.json()["id"]
        
        # Generate content manually
        generate_response = await client.post(
            f"/api/v1/campaigns/{campaign_id}/generate",
            json={"content_count": 10, "preview_only": True}
        )
        
        assert generate_response.status_code == 200
        content = generate_response.json()
        assert len(content["content_preview"]) == 10
        assert all("modern_furniture" in item["theme"] or "home_styling" in item["theme"] 
                  for item in content["content_preview"])
    
    async def test_campaign_roi_calculation(self, client, authenticated_user):
        """Test campaign ROI calculation and analytics."""
        # Create campaign with posts
        campaign_id = await self._create_test_campaign_with_posts(client)
        
        # Simulate campaign performance data
        await self._simulate_campaign_performance(campaign_id)
        
        # Get ROI calculation
        roi_response = await client.get(f"/api/v1/campaigns/{campaign_id}/roi")
        assert roi_response.status_code == 200
        
        roi_data = roi_response.json()
        assert "roi_percentage" in roi_data
        assert "total_investment_cents" in roi_data
        assert "attributed_revenue_cents" in roi_data
        assert "optimization_recommendations" in roi_data
        assert len(roi_data["optimization_recommendations"]) > 0
```

### Campaign Template Testing
```python
class TestCampaignTemplates:
    async def test_template_recommendations(self, client, authenticated_user):
        """Test campaign template recommendations."""
        response = await client.get("/api/v1/campaign-templates", params={
            "objective": "awareness",
            "category": "seasonal"
        })
        
        assert response.status_code == 200
        templates = response.json()
        assert len(templates) > 0
        assert all(template["category"] in ["seasonal", "industry"] for template in templates)
    
    async def test_campaign_from_template(self, client, authenticated_user):
        """Test creating campaign from template."""
        # Get available templates
        templates_response = await client.get("/api/v1/campaign-templates")
        templates = templates_response.json()
        template_id = templates[0]["id"]
        
        # Create campaign from template
        campaign_data = {
            "template_id": template_id,
            "customizations": {
                "name": "Customized Spring Campaign",
                "start_date": "2024-03-01T09:00:00Z",
                "target_reach": 10000
            }
        }
        
        response = await client.post(f"/api/v1/campaigns/from-template/{template_id}", json=campaign_data)
        assert response.status_code == 201
        
        campaign = response.json()
        assert campaign["name"] == "Customized Spring Campaign"
        assert campaign["target_reach"] == 10000
```

### Performance Testing
```python
class TestCampaignPerformance:
    async def test_multi_campaign_performance(self, client, authenticated_user):
        """Test system performance with multiple active campaigns."""
        # Create 10 campaigns with auto-generation
        campaign_ids = []
        for i in range(10):
            response = await client.post("/api/v1/campaigns", json={
                "name": f"Performance Test Campaign {i}",
                "auto_generate_content": True,
                "posts_per_day": 2
            })
            campaign_ids.append(response.json()["id"])
        
        # Activate all campaigns
        start_time = time.time()
        for campaign_id in campaign_ids:
            await client.post(f"/api/v1/campaigns/{campaign_id}/activate")
        activation_time = time.time() - start_time
        
        assert activation_time < 30.0  # Should activate 10 campaigns within 30 seconds
        
        # Test analytics performance
        start_time = time.time()
        for campaign_id in campaign_ids[:5]:  # Test first 5
            await client.get(f"/api/v1/campaigns/{campaign_id}/analytics")
        analytics_time = time.time() - start_time
        
        assert analytics_time < 10.0  # Should get analytics for 5 campaigns within 10 seconds
```

## Performance Benchmarks

### Campaign Operations
- **Campaign Creation**: <2s for campaign with auto-generation
- **Content Generation**: <30s for 20-post campaign
- **Campaign Activation**: <5s including scheduling setup
- **Analytics Calculation**: <3s for 30-day campaign data
- **Template Application**: <1s for template-based campaign creation

### System Scalability
- **Concurrent Campaigns**: Support 50+ active campaigns per user
- **Content Generation**: Handle 1000+ content generations per hour
- **Performance Tracking**: Real-time updates for 100+ active campaigns
- **Template System**: <500ms response for template recommendations

## Risk Mitigation

### Technical Risks
1. **Content Generation Costs**
   - *Risk*: High AI costs for large campaigns
   - *Mitigation*: Cost monitoring, budget limits, content caching

2. **Campaign Coordination Complexity**
   - *Risk*: Multi-post campaigns becoming difficult to manage
   - *Mitigation*: Clear campaign visualization, automated conflict resolution

3. **Performance Tracking Accuracy**
   - *Risk*: Inaccurate ROI calculations affecting business decisions
   - *Mitigation*: Multiple data sources, validation algorithms, audit trails

### Business Risks
1. **Campaign Over-Automation**
   - *Risk*: Campaigns becoming too automated and losing human touch
   - *Mitigation*: Human review options, brand voice validation, quality controls

2. **Template Homogenization**
   - *Risk*: All campaigns looking similar due to template usage
   - *Mitigation*: Customization options, diverse template library, personalization

## Definition of Done

### Functionality
- [ ] Users can create and manage comprehensive marketing campaigns
- [ ] Automated content generation produces high-quality, on-brand content
- [ ] Multi-post campaigns coordinate seamlessly with intelligent scheduling
- [ ] Campaign performance tracking provides accurate ROI calculations
- [ ] Template system enables quick campaign setup with customization

### Quality
- [ ] 95%+ of generated campaign content passes brand compliance
- [ ] Campaign ROI calculations accurate within 5% of actual performance
- [ ] Template-based campaigns achieve performance within 10% of custom campaigns
- [ ] System handles 50+ concurrent campaigns without performance degradation

### User Experience
- [ ] Campaign creation workflow intuitive and efficient
- [ ] Performance dashboards provide actionable insights
- [ ] Template selection helps users choose optimal campaign strategies
- [ ] Campaign management requires minimal manual intervention

### Integration
- [ ] Campaigns integrate seamlessly with existing post management
- [ ] AI-generated content maintains consistency with manual content
- [ ] Performance data feeds back into optimization algorithms
- [ ] Template system learns from successful campaign patterns

## Sprint Review & Retrospective

### Demo Checklist
- [ ] Create complete marketing campaign from template
- [ ] Show automated content generation and scheduling
- [ ] Demonstrate campaign performance tracking and ROI calculation
- [ ] Display campaign optimization recommendations
- [ ] Present template creation from successful campaign

### Key Metrics to Review
- Campaign creation success rate and user adoption
- Content generation quality scores and user satisfaction
- Campaign performance improvement vs manual management
- Template usage rates and customization patterns
- System performance under multiple active campaigns

## Handoff to Sprint 6

### Deliverables for Next Sprint
- [ ] Complete campaign system ready for production deployment
- [ ] Performance monitoring prepared for production scale
- [ ] Template library established with proven campaign patterns
- [ ] Optimization algorithms ready for continuous improvement

### Next Sprint Preparation
- [ ] Production deployment planning and infrastructure scaling
- [ ] Performance optimization and monitoring enhancement
- [ ] User onboarding and documentation finalization
- [ ] Sprint 6 detailed task planning for production readiness