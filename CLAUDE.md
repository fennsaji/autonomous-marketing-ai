# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an autonomous Instagram marketing system for the Defeah home decor brand. The project has evolved from documentation and architectural designs to a **fully implemented FastAPI-based backend system** with comprehensive authentication, testing framework, and quality assurance pipeline.

## Current Implementation Status

✅ **Sprint 1 COMPLETED** - Foundation & Core Setup (95% complete)
- Epic 1: Project Infrastructure Setup (100%)
- Epic 2: Database Foundation (100%)
- Epic 3: Authentication System (100%)
- Epic 4: API Framework & Documentation (100%)
- Epic 5: Testing & Quality Assurance (100%)

## Project Structure

This repository contains:
- **docs/**: Complete project documentation including product specifications, technical designs, and development guides
- **backend/**: Full FastAPI implementation with comprehensive testing suite
- **README.md**: Basic project information and disclaimer

### Key Documentation Files
- `docs/product_specification.md`: Complete technical and strategic foundation for Instagram marketing automation
- `docs/backend_design.md`: Comprehensive FastAPI backend architecture and implementation details
- `docs/development_docs.md`: Development environment setup, coding standards, and workflows
- `docs/development-roadmap/sprints/sprint-1-foundation.md`: Detailed Sprint 1 implementation plan

### Implementation Structure
- **backend/app/**: Core FastAPI application following Clean Architecture principles
  - `core/`: Configuration, security, and database engine
  - `models/`: SQLAlchemy database models
  - `schemas/`: Pydantic request/response validation
  - `services/`: Business logic layer (Service Layer Pattern)
  - `routers/`: API endpoint definitions
  - `utils/`: Utility functions and helpers
- **backend/tests/**: World-class testing suite with 150+ test cases
  - Unit tests, integration tests, security tests, performance tests
  - 95%+ code coverage with pytest and advanced testing patterns
- **backend/migrations/**: Alembic database migrations

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

The backend implementation is complete with a comprehensive development environment. Use these commands from the `backend/` directory:

### Environment Setup
```bash
# Start all services (PostgreSQL, Redis, FastAPI)
docker-compose up -d

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks
pre-commit install
```

### Development Server
```bash
# Run FastAPI development server with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Database migrations
alembic upgrade head
```

### Testing & Quality Assurance
```bash
# Run all tests with coverage
make test-coverage

# Run specific test categories
make test-unit          # Unit tests only
make test-integration   # Integration tests only
make test-security      # Security tests only
make test-performance   # Performance tests only
make test-async         # Async operation tests

# Code quality checks
make lint              # Flake8 linting
make format            # Black + isort formatting
make type-check        # MyPy type checking
make security          # Bandit security scanning
make all-checks        # All quality checks

# Epic 5 validation (comprehensive QA)
make validate-epic5
```

### Available API Endpoints
```bash
# Authentication
POST /api/v1/auth/register     # User registration
POST /api/v1/auth/login        # User login
POST /api/v1/auth/refresh      # Token refresh
POST /api/v1/auth/logout       # User logout
GET  /api/v1/auth/me           # Current user profile

# System
GET  /health                   # Health check
GET  /docs                     # Interactive API docs
GET  /openapi.json             # OpenAPI specification
```

## Key Design Patterns & Principles

### Clean Architecture Implementation
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DRY Principle**: Don't Repeat Yourself - shared utilities and base classes
- **Service Layer Pattern**: Business logic encapsulated in dedicated service classes
- **Repository Pattern**: Data access abstraction with async SQLAlchemy
- **Dependency Injection**: FastAPI's dependency system for clean separation

### Code Quality Standards
- **Type Safety**: Comprehensive type hints with MyPy validation
- **Input Validation**: Pydantic schemas for request/response validation
- **Error Handling**: Structured exception handling with detailed error responses
- **Security**: JWT authentication, input sanitization, SQL injection prevention
- **Testing**: 95%+ coverage with unit, integration, security, and performance tests

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

## Sprint 1 Achievements

### Technical Excellence
- ✅ **World-Class Testing Framework**: 150+ test cases with 95%+ coverage
- ✅ **Security-First Design**: SQL injection prevention, input sanitization, JWT security
- ✅ **Performance Optimized**: Async database operations, connection pooling, Redis caching
- ✅ **Quality Assurance Pipeline**: Pre-commit hooks, automated linting, type checking
- ✅ **Clean Code Standards**: SOLID principles, DRY implementation, comprehensive documentation

### Infrastructure Foundation
- ✅ **Containerized Environment**: Docker Compose with PostgreSQL, Redis, FastAPI
- ✅ **Database Foundation**: SQLAlchemy models, Alembic migrations, connection management
- ✅ **API Documentation**: Auto-generated OpenAPI with Swagger UI
- ✅ **Authentication System**: JWT tokens, refresh mechanism, secure password hashing

### Testing Categories Implemented
- **Unit Tests**: 45+ tests for authentication utilities and business logic
- **Integration Tests**: 35+ tests for all API endpoints with database operations
- **Security Tests**: 25+ tests for SQL injection, XSS prevention, input validation
- **Performance Tests**: 20+ tests with response time validation and benchmarking
- **Async Tests**: 15+ tests for database and Redis operations
- **Redis Integration**: 10+ tests for token blacklisting and session management

## Next Phase: Sprint 2 Preparation

With Sprint 1 foundation complete, the system is ready for:
1. **Instagram API Integration**: OAuth 2.0 flow and Graph API connectivity
2. **Content Management**: Post creation, scheduling, and media handling
3. **AI Integration**: OpenAI GPT-4 for captions, DALL-E 3 for image generation

The robust foundation ensures scalable development with maintained code quality and security standards.