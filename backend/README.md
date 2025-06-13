# Defeah Marketing Backend

FastAPI-based backend for autonomous Instagram marketing system for Defeah home decor brand.

## Features

- **User Management**: Registration, authentication, and profile management
- **Instagram Integration**: OAuth connection and automated posting
- **AI Content Generation**: GPT-4 for captions, DALL-E 3 for images, hashtag suggestions
- **Campaign Management**: Automated content campaigns with scheduling
- **Analytics**: Performance tracking and insights
- **Background Tasks**: Celery-based task queue for automation

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Cache**: Redis
- **Task Queue**: Celery
- **AI Integration**: OpenAI GPT-4 and DALL-E 3
- **Authentication**: JWT with bcrypt password hashing

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API route handlers
│   ├── core/            # Core configuration and utilities
│   ├── models/          # SQLAlchemy database models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic services
│   ├── tasks/           # Celery background tasks
│   └── utils/           # Utility functions
├── migrations/          # Alembic database migrations
├── tests/              # Test suite
└── docker-compose.yml  # Docker development setup
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Environment Setup

1. **Clone and setup:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Database setup:**
   ```bash
   # Create database
   createdb defeah_marketing
   
   # Run migrations
   alembic upgrade head
   ```

4. **Start the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Configuration

Key environment variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/defeah_marketing

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key-here

# Instagram/Facebook
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret

# OpenAI
OPENAI_API_KEY=your-openai-api-key
```

## API Documentation

Once running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **API info**: http://localhost:8000/info
- **Health check**: http://localhost:8000/health

## Key API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/instagram/connect` - Connect Instagram account

### Posts Management
- `GET /api/v1/posts` - List user posts
- `POST /api/v1/posts` - Create new post
- `POST /api/v1/posts/{id}/publish` - Publish post to Instagram

### AI Content Generation
- `POST /api/v1/content/caption/generate` - Generate captions
- `POST /api/v1/content/image/generate` - Generate images
- `POST /api/v1/content/hashtags/suggest` - Suggest hashtags

### Campaign Management
- `GET /api/v1/campaigns` - List campaigns
- `POST /api/v1/campaigns` - Create campaign
- `GET /api/v1/campaigns/{id}/analytics` - Campaign analytics

## Background Tasks

The system uses Celery for background processing:

- **Post Publishing**: Automated Instagram posting
- **Analytics Sync**: Regular performance data updates
- **Content Generation**: Automated campaign content creation
- **Token Refresh**: Instagram token management

### Running Celery

```bash
# Worker
celery -A app.tasks.celery_app worker --loglevel=info

# Beat scheduler
celery -A app.tasks.celery_app beat --loglevel=info
```

## Database

### Models

- **User**: User accounts and Instagram integration
- **Post**: Instagram posts with content and analytics
- **Campaign**: Marketing campaigns with automation settings
- **AnalyticsEvent**: Individual performance metrics
- **PerformanceMetrics**: Aggregated analytics data

### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Services

### Instagram Service
Handles Instagram Graph API integration:
- OAuth authentication
- Media publishing
- Analytics retrieval
- Token refresh

### OpenAI Service
Manages AI content generation:
- Caption generation with GPT-4
- Image generation with DALL-E 3
- Hashtag suggestions
- Content performance analysis

## Security

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt for secure password storage
- **Rate Limiting**: API and Instagram rate limit protection
- **Input Validation**: Comprehensive Pydantic validation
- **CORS**: Configurable cross-origin resource sharing

## Development

### Code Quality

```bash
# Format code
black app/
isort app/

# Linting
flake8 app/

# Type checking
mypy app/
```

### Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Deployment

The application is containerized and ready for deployment:

- **Production Dockerfile** with security best practices
- **Multi-stage builds** for optimized images
- **Health checks** for container orchestration
- **Environment-based configuration**

## Monitoring

Built-in monitoring capabilities:
- Health check endpoints
- Structured logging
- Performance metrics
- Error tracking integration

## License

Private - Defeah Home Decor Brand

## Support

For development support, refer to the comprehensive documentation in the `docs/` folder.