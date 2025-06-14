# Defeah Marketing Backend

Autonomous Instagram Marketing System for Defeah Home Decor - Backend API

## 📋 Project Overview

An AI-powered Instagram marketing automation system designed specifically for the Defeah home decor brand. This backend API provides comprehensive functionality for:

- **AI Content Generation**: Automated caption and image creation using GPT-4 and DALL-E 3
- **Instagram Integration**: OAuth authentication and automated post publishing
- **Campaign Management**: Multi-post marketing campaigns with performance tracking
- **Analytics & Insights**: Detailed engagement metrics and ROI analysis
- **Smart Scheduling**: Optimal timing for maximum audience engagement

The system enables autonomous Instagram marketing while maintaining brand consistency and compliance with platform policies.

## ⚠️ Disclaimer

**This project is fully developed by Large Language Models (LLMs) as a demonstration of AI-powered software development capabilities. The entire codebase, architecture, documentation, and implementation have been generated through AI assistance without human coding intervention.**

This serves as an educational example of:
- AI-driven software architecture and development
- Automated code generation for complex systems
- LLM capabilities in understanding and implementing business requirements
- Modern development practices applied through AI assistance

**Note**: While functional, this is a demonstration project and should be thoroughly reviewed, tested, and adapted before any production use.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

### Environment Setup

1. **Clone and navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

3. **For local development (recommended for testing):**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start server
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
   ```

4. **Or start all services with Docker Compose:**
   ```bash
   docker compose up --build
   ```

5. **Verify setup:**
   - API: http://localhost:8080
   - API Documentation: http://localhost:8080/docs
   - Health Check: http://localhost:8080/health

### ✅ **Verification Tests**

Test the API endpoints:

```bash
# Test root endpoint
curl http://localhost:8080/

# Expected response:
# {"message":"Defeah Marketing Backend","version":"1.0.0","environment":"development","docs_url":"/docs"}

# Test health check
curl http://localhost:8080/health

# Expected response:
# {"status":"healthy","services":{"database":"connected","redis":"connected"}}
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── api/           # API route handlers
│   │   └── v1/        # API version 1
│   ├── core/          # Core functionality
│   │   ├── config.py  # Settings management
│   │   ├── database.py # Database configuration
│   │   └── redis.py   # Redis configuration
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── utils/         # Utility functions
│   └── main.py        # FastAPI application
├── docker-compose.yml # Docker services
├── Dockerfile         # FastAPI container
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🛠️ Development

### Local Development (without Docker)

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start PostgreSQL and Redis (Docker):**
   ```bash
   docker-compose up db redis
   ```

4. **Run FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Database Setup

The database is automatically configured when using Docker Compose. For local development:

```bash
# Create database (if not using Docker)
createdb defeah_marketing

# Update .env with your database URL
DATABASE_URL=postgresql://postgres:password@localhost:5432/defeah_marketing
```

## 🔧 Configuration

Configuration is managed through environment variables. See `.env.example` for all available options:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string  
- `DEBUG`: Enable debug mode
- `SECRET_KEY`: Application secret key

## 🧪 Testing Setup

The project infrastructure supports testing but test implementation is planned for later sprints.

## 📚 API Documentation

When running in development mode:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up

# Start with rebuild
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🔍 Health Checks

- **Application Health**: `GET /health`
- **Root Info**: `GET /`

## 🚦 Service Ports

- **FastAPI**: http://localhost:8080
- **PostgreSQL**: localhost:5433 
- **Redis**: localhost:6379

## 🎯 Current Implementation Status

**Sprint 1 Epic 1: Project Infrastructure Setup - ✅ COMPLETE**

- ✅ Project directory structure
- ✅ Docker and Docker Compose setup
- ✅ FastAPI application with hot reload
- ✅ PostgreSQL and Redis integration
- ✅ Environment variable management
- ✅ Logging and error handling

## 🔄 Next Steps

**Epic 2: Database Foundation**
- Database models creation
- Alembic migrations setup
- Initial user model

## 🆘 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8080, 5433, and 6379 are available
2. **Docker permission issues**: Make sure Docker daemon is running
3. **Database connection**: Check PostgreSQL is running and accessible

### Logs

```bash
# View application logs
docker-compose logs web

# View database logs  
docker-compose logs db

# View all logs
docker-compose logs
```

## 📝 Development Notes

- FastAPI automatically reloads when code changes (in Docker development mode)
- Database tables are automatically created on startup
- Redis connection is tested on startup
- All configurations use environment variables for flexibility