# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an autonomous Instagram marketing system for the Defeah home decor brand. The project consists of documentation and architectural designs for a comprehensive FastAPI-based backend system with AI-powered content generation and Instagram API integration.

## Project Structure

This repository contains:
- **docs/**: Complete project documentation including product specifications, technical designs, and development guides
- **README.md**: Basic project information and disclaimer

Key documentation files:
- `docs/product_specification.md`: Complete technical and strategic foundation for Instagram marketing automation
- `docs/backend_design.md`: Comprehensive FastAPI backend architecture and implementation details
- `docs/development_docs.md`: Development environment setup, coding standards, and workflows

## Architecture Overview

The system is designed around these core components:

### Backend Architecture (FastAPI)
- **FastAPI Web Framework**: RESTful API with automatic OpenAPI documentation
- **PostgreSQL Database**: Primary data store with SQLAlchemy ORM
- **Redis Cache**: Session management and caching layer
- **Celery Task Queue**: Asynchronous processing for post scheduling and analytics
- **Instagram Graph API**: Official Instagram integration for posting and analytics
- **OpenAI Integration**: GPT-4 for caption generation, DALL-E 3 for image creation

### Key Services
- **Authentication Service**: JWT-based auth with Instagram OAuth integration
- **Post Management**: Content creation, scheduling, and publishing
- **Analytics Service**: Performance tracking and insights generation
- **AI Content Generation**: Automated caption and image creation
- **Campaign Management**: Multi-post campaign orchestration

### Database Design
- **Users**: Account management and Instagram credentials
- **Posts**: Content storage with metadata and analytics
- **Campaigns**: Multi-post marketing campaign coordination
- **Analytics Events**: Detailed engagement tracking and performance metrics

## Development Commands

Since this is currently a documentation-only repository, there are no build, test, or development commands available yet. The documentation provides complete implementation guidance for when development begins.

When implementation starts, typical commands would include:
- Backend: `uvicorn app.main:app --reload` (FastAPI development server)
- Database: `alembic upgrade head` (database migrations)
- Tasks: `celery -A app.tasks.celery_app worker --loglevel=info` (background tasks)
- Tests: `pytest` (backend testing)

## Key Design Patterns

### Service Layer Architecture
- Services encapsulate business logic
- Models define database schemas
- Schemas handle API validation
- Router modules organize endpoints

### Instagram API Integration
- Rate limiting with exponential backoff
- Token refresh automation
- Compliance with Meta developer policies
- FTC disclosure requirements for AI-generated content

### AI Integration Strategy
- Cost-optimized content generation pipeline
- Multiple AI providers (OpenAI, potential Stable Diffusion)
- Brand voice consistency across generated content
- Performance analytics for content optimization

## Security Considerations

- JWT token-based authentication
- Instagram OAuth 2.0 integration
- API rate limiting and circuit breakers
- Input validation and sanitization
- Secure environment variable management
- FTC compliance for AI-generated content disclosure

## Compliance & Safety

### Instagram Platform Compliance
- Respect rate limits (200 calls/user/hour, 50 posts/day)
- Human-like posting patterns
- Avoid engagement pods and artificial interactions
- Regular monitoring using Instagram Account Status

### Legal Compliance
- AI content disclosure requirements
- FTC penalty avoidance (up to $51,744 per violation)
- Privacy policy and data usage transparency
- Commercial use rights for generated content

## Performance Optimization

### Database Optimization
- Connection pooling and query optimization
- Strategic indexing on filtered columns
- Efficient pagination for large datasets
- Multi-touch attribution for analytics

### Caching Strategy
- Redis for session management
- API response caching for expensive operations
- Instagram analytics data caching
- Content generation result caching

## Future Implementation Notes

The documentation provides a complete roadmap for implementation in 3 phases:
1. **Foundation** (Months 1-2): Basic API and AI integration
2. **Enhancement** (Months 3-4): Advanced features and analytics
3. **Scale** (Months 5-6): Multi-account management and optimization

The system is designed to handle enterprise-scale Instagram marketing while maintaining platform compliance and maximizing ROI through AI-powered content creation and data-driven optimization.