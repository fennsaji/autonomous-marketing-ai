# Contributing to Defeah Marketing Backend

Thank you for your interest in contributing to the Defeah Autonomous Instagram Marketing System! This guide will help you get started with contributing to this AI-generated project.

## 🤖 Project Context

**Important**: This project is fully developed by Large Language Models (LLMs) as a demonstration of AI-powered software development. While we welcome contributions, please keep in mind this is primarily an educational showcase of AI development capabilities.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Process](#contribution-process)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Code Review Guidelines](#code-review-guidelines)

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- Basic understanding of FastAPI, SQLAlchemy, and PostgreSQL

### First Time Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/autonomous-marketing-ai.git
   cd autonomous-marketing-ai/backend
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start development services**
   ```bash
   docker compose up -d db redis
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
   ```

5. **Verify setup**
   ```bash
   curl http://localhost:8080/health
   ```

## 🛠️ Development Setup

### Environment Configuration

1. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

2. **Configure your environment**
   ```bash
   # Edit .env with your settings
   DATABASE_URL=postgresql://postgres:password@localhost:5433/defeah_marketing
   REDIS_URL=redis://localhost:6379/0
   DEBUG=true
   ```

### Development Tools

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

This includes:
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking
- `pytest` - Testing framework
- `pre-commit` - Git hooks

### Pre-commit Hooks

Set up pre-commit hooks to ensure code quality:
```bash
pre-commit install
```

## 🔄 Contribution Process

### 1. Issue Creation

Before starting work:
- Check existing issues to avoid duplication
- Create a new issue describing your contribution
- Wait for maintainer feedback/approval for significant changes

### 2. Branch Creation

Create a feature branch from `main`:
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `test/description` - Testing improvements
- `refactor/description` - Code refactoring

### 3. Development

Follow the development workflow:
1. Make your changes
2. Write/update tests
3. Update documentation
4. Run quality checks
5. Commit your changes

## 📝 Code Standards

### Code Formatting

We use **Black** for consistent code formatting:
```bash
# Format all code
black app/ tests/

# Check formatting
black --check app/ tests/
```

### Linting

We use **flake8** for linting:
```bash
# Run linting
flake8 app/ tests/

# Configuration in setup.cfg
```

### Type Checking

We use **mypy** for type checking:
```bash
# Run type checking
mypy app/
```

### Code Style Guidelines

#### General Principles
- Write clear, readable, and maintainable code
- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Keep functions small and focused
- Add docstrings to all public functions and classes

#### FastAPI Specific
```python
# Good: Clear endpoint definition
@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """Create a new user account."""
    # Implementation here
```

#### Database Models
```python
# Good: Clear model definition with proper typing
class User(Base):
    """User model for authentication and profile management."""
    
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

#### Error Handling
```python
# Good: Specific exception handling
try:
    user = await user_service.create_user(user_data)
except UserAlreadyExistsException:
    raise HTTPException(status_code=400, detail="Email already registered")
except Exception as e:
    logger.error(f"User creation failed: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

## 🧪 Testing Requirements

### Test Coverage

- **Minimum Coverage**: 80% overall
- **Core Logic**: 90% coverage required
- **API Endpoints**: 85% coverage required

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest -m "unit"
pytest -m "integration"
```

### Writing Tests

#### Unit Tests
```python
# tests/unit/test_user_service.py
import pytest
from app.services.user_service import UserService
from app.schemas.user import UserCreate

@pytest.mark.unit
def test_create_user_success():
    """Test successful user creation."""
    # Arrange
    user_data = UserCreate(email="test@example.com", password="password123")
    
    # Act
    result = UserService.validate_user_data(user_data)
    
    # Assert
    assert result.email == "test@example.com"
```

#### Integration Tests
```python
# tests/integration/test_api_users.py
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
def test_create_user_endpoint(client: TestClient):
    """Test user creation API endpoint."""
    response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

### Test Requirements for PRs

- All new code must have corresponding tests
- Tests must pass in CI/CD pipeline
- Coverage thresholds must be maintained
- Integration tests for new API endpoints

## 📚 Documentation

### Code Documentation

#### Docstrings
```python
def create_user(user_data: UserCreate) -> User:
    """
    Create a new user account.
    
    Args:
        user_data: User creation data containing email, password, and profile info
        
    Returns:
        User: The created user object with generated ID and timestamps
        
    Raises:
        UserAlreadyExistsException: If email is already registered
        ValidationException: If user data is invalid
    """
```

#### Type Hints
```python
# Always include type hints
def process_campaign_data(
    campaign_id: uuid.UUID,
    user: User,
    db: Session
) -> Optional[Campaign]:
    """Process campaign data with proper typing."""
```

### API Documentation

- All endpoints must be documented with OpenAPI/Swagger
- Include request/response examples
- Document error responses
- Add detailed descriptions

### Updating Documentation

When making changes:
1. Update relevant documentation files
2. Update API documentation if endpoints change
3. Update README if setup process changes
4. Add changelog entries for significant changes

## 🔄 Pull Request Process

### Before Submitting

1. **Sync with main branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Run quality checks**
   ```bash
   # Format code
   black app/ tests/
   
   # Run linting
   flake8 app/ tests/
   
   # Run type checking
   mypy app/
   
   # Run tests
   pytest --cov=app
   ```

3. **Update documentation**
   - Update relevant docs
   - Add/update tests
   - Update CHANGELOG.md

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass
- [ ] Coverage maintained/improved

## Documentation
- [ ] Code documented
- [ ] API docs updated
- [ ] README updated (if needed)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No merge conflicts
- [ ] CI/CD pipeline passes
```

### PR Review Process

1. **Automated Checks**: All CI/CD checks must pass
2. **Code Review**: At least one approving review required
3. **Testing**: Manual testing for significant changes
4. **Documentation**: Documentation review for user-facing changes

## 👥 Code Review Guidelines

### For Authors

- Provide clear PR descriptions
- Respond to feedback promptly
- Make requested changes
- Keep PRs focused and reasonably sized

### For Reviewers

#### What to Look For

1. **Functionality**
   - Does the code work as intended?
   - Are edge cases handled?
   - Is error handling appropriate?

2. **Code Quality**
   - Is the code readable and maintainable?
   - Are naming conventions followed?
   - Is the code properly structured?

3. **Testing**
   - Are there adequate tests?
   - Do tests cover edge cases?
   - Is coverage maintained?

4. **Security**
   - Are there any security vulnerabilities?
   - Is sensitive data handled properly?
   - Are inputs properly validated?

5. **Performance**
   - Are there any performance issues?
   - Are database queries optimized?
   - Is caching used appropriately?

#### Review Comments

- Be constructive and specific
- Explain the reasoning behind suggestions
- Distinguish between blocking issues and suggestions
- Acknowledge good code and improvements

## 🐛 Bug Reports

When reporting bugs, include:

1. **Environment Information**
   - Python version
   - Operating system
   - Dependencies versions

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Minimal reproducible example
   - Expected vs actual behavior

3. **Additional Context**
   - Error messages and stack traces
   - Screenshots (if applicable)
   - Related issues or PRs

## 💡 Feature Requests

When requesting features:

1. **Use Case**: Explain the problem you're trying to solve
2. **Proposed Solution**: Describe your ideal solution
3. **Alternatives**: Consider alternative approaches
4. **Impact**: Explain who would benefit from this feature

## 📞 Getting Help

- **Documentation**: Check existing docs first
- **Issues**: Search existing issues for similar problems
- **Discussions**: Use GitHub Discussions for questions
- **Discord**: Join our community Discord (if available)

## 🎯 Development Priorities

Current development focus areas:

1. **Sprint 1 Completion**
   - Database foundation
   - Authentication system
   - Testing framework
   - API documentation

2. **Quality Improvements**
   - Test coverage improvements
   - Performance optimization
   - Security enhancements
   - Documentation updates

3. **Future Features**
   - Instagram integration
   - AI content generation
   - Campaign management
   - Analytics dashboard

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- Project documentation

Thank you for contributing to this AI-generated software development showcase!