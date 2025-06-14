"""
Pytest configuration and fixtures.
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db, get_async_db

# Test database URLs
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5433/defeah_marketing_test"
SQLALCHEMY_ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5433/defeah_marketing_test"

# Create test database engines
engine = create_engine(SQLALCHEMY_DATABASE_URL)
async_engine = create_async_engine(SQLALCHEMY_ASYNC_DATABASE_URL, echo=False)

# Create test sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingAsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


async def override_get_async_db():
    """Override async database dependency for testing."""
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
async def async_db_session():
    """Create a fresh async database session for each test."""
    # Create tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestingAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
    
    # Drop tables after test
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override."""
    # Override the database dependencies
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_async_db] = override_get_async_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }


@pytest.fixture
def sample_user_login_data():
    """Sample user login data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }


@pytest.fixture
def sample_weak_password_data():
    """Sample user data with weak password for testing."""
    return {
        "email": "weak@example.com",
        "password": "weak",
        "full_name": "Weak Password User"
    }


@pytest.fixture
def sample_invalid_email_data():
    """Sample user data with invalid email for testing."""
    return {
        "email": "invalid-email",
        "password": "TestPassword123!",
        "full_name": "Invalid Email User"
    }


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()