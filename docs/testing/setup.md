# Testing Setup Guide

Complete guide for setting up the testing environment for the Defeah Marketing Backend.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (for local testing)
- Redis (for local testing)

## Installation

### 1. Install Testing Dependencies

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx pytest-mock factory-boy freezegun
```

### 2. Update requirements.txt

Add testing dependencies to `backend/requirements-test.txt`:

```txt
# Testing framework
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0

# HTTP testing
httpx==0.25.2

# Test utilities
factory-boy==3.3.0
freezegun==1.2.2
faker==20.1.0

# Database testing
pytest-postgresql==5.0.0
sqlalchemy-utils==0.41.1

# Performance testing
pytest-benchmark==4.0.0

# Security testing
bandit==1.7.5
safety==2.3.5
```

### 3. Create pytest Configuration

Create `backend/pytest.ini`:

```ini
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
    --cov-report=html:htmlcov
    --cov-report=xml:coverage.xml
    --cov-fail-under=80
    --asyncio-mode=auto
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    auth: Authentication related tests
    api: API endpoint tests
    db: Database related tests
```

## Test Directory Structure

Create the following test directory structure in `backend/`:

```
tests/
├── __init__.py
├── conftest.py                 # Shared fixtures and configuration
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_models.py
│   ├── test_utils.py
│   └── core/
│       ├── test_config.py
│       ├── test_database.py
│       └── test_security.py
├── integration/                # Integration tests
│   ├── __init__.py
│   ├── test_api_auth.py
│   ├── test_api_health.py
│   ├── test_database_ops.py
│   └── test_redis_ops.py
├── e2e/                       # End-to-end tests
│   ├── __init__.py
│   ├── test_user_journey.py
│   └── test_instagram_flow.py
├── fixtures/                  # Test data and fixtures
│   ├── __init__.py
│   ├── users.py
│   ├── campaigns.py
│   └── responses/
│       ├── instagram_api.json
│       └── openai_api.json
└── utils/                     # Test utilities
    ├── __init__.py
    ├── helpers.py
    ├── factories.py
    └── mocks.py
```

## Test Configuration

### 1. Create conftest.py

Create `backend/tests/conftest.py`:

```python
"""
Pytest configuration and shared fixtures.
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }


@pytest.fixture
def mock_instagram_response():
    """Mock Instagram API response data."""
    return {
        "access_token": "test_token_12345",
        "token_type": "bearer",
        "expires_in": 3600
    }


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response data."""
    return {
        "choices": [
            {
                "message": {
                    "content": "Beautiful home decor inspiration for your Instagram feed! 🏡✨ #homedecor #interior"
                }
            }
        ]
    }
```

### 2. Environment Configuration

Create `backend/.env.test`:

```bash
# Test Environment Configuration
ENVIRONMENT=testing
DEBUG=true

# Test Database
DATABASE_URL=sqlite:///./test.db

# Test Redis (use different DB)
REDIS_URL=redis://localhost:6379/1

# Test Security
SECRET_KEY=test-secret-key-for-testing-only

# Disable external services in tests
INSTAGRAM_CLIENT_ID=test_client_id
INSTAGRAM_CLIENT_SECRET=test_client_secret
OPENAI_API_KEY=test_openai_key

# Test-specific settings
TESTING=true
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_auth.py

# Run specific test function
pytest tests/unit/test_auth.py::test_user_registration

# Run tests by marker
pytest -m "unit"
pytest -m "integration"
pytest -m "auth"
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# View coverage in browser
open htmlcov/index.html

# Generate terminal coverage report
pytest --cov=app --cov-report=term-missing

# Generate XML coverage for CI
pytest --cov=app --cov-report=xml
```

### Test Categories

```bash
# Run only unit tests
pytest tests/unit/ -m unit

# Run only integration tests
pytest tests/integration/ -m integration

# Run only end-to-end tests
pytest tests/e2e/ -m e2e

# Skip slow tests
pytest -m "not slow"
```

## Docker Test Environment

### 1. Create docker-compose.test.yml

```yaml
version: '3.8'

services:
  test-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: defeah_marketing_test
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5434:5432"
    
  test-redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"
    
  test-runner:
    build: .
    depends_on:
      - test-db
      - test-redis
    environment:
      - DATABASE_URL=postgresql://postgres:password@test-db:5432/defeah_marketing_test
      - REDIS_URL=redis://test-redis:6379/0
      - ENVIRONMENT=testing
    volumes:
      - ./app:/app/app
      - ./tests:/app/tests
    command: pytest -v --cov=app --cov-report=term-missing
```

### 2. Run Tests in Docker

```bash
# Start test environment
docker-compose -f docker-compose.test.yml up --build

# Run tests only
docker-compose -f docker-compose.test.yml run test-runner

# Cleanup
docker-compose -f docker-compose.test.yml down
```

## Test Data Management

### 1. Create Test Factories

Create `backend/tests/utils/factories.py`:

```python
"""
Test data factories for generating test objects.
"""
import factory
from faker import Faker
from app.models.user import User

fake = Faker()


class UserFactory(factory.Factory):
    """Factory for creating test users."""
    
    class Meta:
        model = User
    
    email = factory.LazyAttribute(lambda obj: fake.email())
    full_name = factory.LazyAttribute(lambda obj: fake.name())
    hashed_password = factory.LazyAttribute(lambda obj: fake.password())
    is_active = True
    is_verified = False


class InstagramUserFactory(UserFactory):
    """Factory for users with Instagram connection."""
    
    instagram_user_id = factory.LazyAttribute(lambda obj: fake.uuid4())
    instagram_username = factory.LazyAttribute(lambda obj: fake.user_name())
    instagram_connected = True
```

### 2. Create Mock Utilities

Create `backend/tests/utils/mocks.py`:

```python
"""
Mock utilities for external services.
"""
from unittest.mock import AsyncMock, Mock
import json


class MockInstagramAPI:
    """Mock Instagram API responses."""
    
    @staticmethod
    def oauth_token_response():
        return {
            "access_token": "test_token_12345",
            "token_type": "bearer",
            "expires_in": 3600
        }
    
    @staticmethod
    def user_profile_response():
        return {
            "id": "17841400455970022",
            "username": "test_user",
            "account_type": "BUSINESS"
        }
    
    @staticmethod
    def publish_photo_response():
        return {
            "id": "17895695668004550"
        }


class MockOpenAI:
    """Mock OpenAI API responses."""
    
    @staticmethod
    def chat_completion_response():
        return {
            "choices": [
                {
                    "message": {
                        "content": "Beautiful home decor inspiration! 🏡✨ #homedecor #interior"
                    }
                }
            ]
        }
    
    @staticmethod
    def image_generation_response():
        return {
            "data": [
                {
                    "url": "https://example.com/generated-image.jpg"
                }
            ]
        }
```

## Continuous Integration Setup

### 1. GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: defeah_marketing_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:password@localhost:5432/defeah_marketing_test
        REDIS_URL: redis://localhost:6379/1
        ENVIRONMENT: testing
      run: |
        cd backend
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: backend/coverage.xml
        flags: unittests
```

## Pre-commit Hooks

### 1. Install pre-commit

```bash
pip install pre-commit
```

### 2. Create .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        args: [--line-length=88]
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]
  
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: bash -c 'cd backend && pytest'
        language: system
        pass_filenames: false
        always_run: true
```

### 3. Install hooks

```bash
pre-commit install
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check if PostgreSQL is running
   brew services start postgresql
   
   # Reset test database
   dropdb defeah_marketing_test
   createdb defeah_marketing_test
   ```

2. **Redis Connection Issues**
   ```bash
   # Check if Redis is running
   brew services start redis
   
   # Test Redis connection
   redis-cli ping
   ```

3. **Import Errors**
   ```bash
   # Add current directory to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   
   # Or run with Python module
   python -m pytest
   ```

4. **Coverage Issues**
   ```bash
   # Clear coverage cache
   rm -rf .coverage htmlcov/
   
   # Run with fresh coverage
   pytest --cov=app --cov-report=html
   ```

### Performance Optimization

1. **Parallel Test Execution**
   ```bash
   # Install pytest-xdist
   pip install pytest-xdist
   
   # Run tests in parallel
   pytest -n auto
   ```

2. **Test Selection**
   ```bash
   # Run only failed tests
   pytest --lf
   
   # Run changed tests only
   pytest --testmon
   ```

3. **Database Optimization**
   ```bash
   # Use in-memory SQLite for faster tests
   export DATABASE_URL="sqlite:///:memory:"
   ```

This setup provides a comprehensive testing foundation that aligns with Sprint 1 Epic 5 requirements and supports the development workflow outlined in the project documentation.