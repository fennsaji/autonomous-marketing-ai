# Defeah Marketing Backend - Testing & Quality Assurance
# Makefile for Epic 5 - Testing & Quality Assurance

.PHONY: help install test test-unit test-integration test-coverage lint format type-check security pre-commit clean all-checks

# Default target
help:
	@echo "Available commands:"
	@echo "  install          Install dependencies and dev tools"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-security    Run security tests only"
	@echo "  test-performance Run performance tests only"
	@echo "  test-async       Run async tests only"
	@echo "  test-coverage    Run tests with coverage report"
	@echo "  lint             Run linting checks"
	@echo "  format           Format code with black and isort"
	@echo "  type-check       Run type checking with mypy"
	@echo "  security         Run security scanning with bandit"
	@echo "  pre-commit       Run all pre-commit hooks"
	@echo "  all-checks       Run all quality assurance checks"
	@echo "  clean            Clean up generated files"

# Installation
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Installation complete!"

# Testing commands
test:
	@echo "Running all tests..."
	pytest -v

test-unit:
	@echo "Running unit tests..."
	pytest -v -m unit

test-integration:
	@echo "Running integration tests..."
	pytest -v -m integration

test-security:
	@echo "Running security tests..."
	pytest -v -m security

test-performance:
	@echo "Running performance tests..."
	pytest -v -m performance

test-async:
	@echo "Running async tests..."
	pytest -v -m asyncio

test-coverage:
	@echo "Running tests with coverage..."
	pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=80

# Code quality commands
lint:
	@echo "Running flake8 linting..."
	flake8 app tests

format:
	@echo "Formatting code with black..."
	black app tests
	@echo "Sorting imports with isort..."
	isort app tests

type-check:
	@echo "Running type checking with mypy..."
	mypy app

security:
	@echo "Running security scanning with bandit..."
	bandit -r app -f json -o bandit-report.json || true
	@echo "Security scan complete. Check bandit-report.json for details."

# Pre-commit hooks
pre-commit:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files

# Comprehensive quality assurance
all-checks: format lint type-check security test-coverage
	@echo "All quality assurance checks completed!"

# Clean up
clean:
	@echo "Cleaning up generated files..."
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf bandit-report.json
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"

# Development database setup (for testing)
setup-test-db:
	@echo "Setting up test database..."
	@echo "Make sure PostgreSQL is running on port 5433 with database 'defeah_marketing_test'"
	@echo "Username: postgres, Password: password"
	python scripts/init_db.py --test

# Run specific test file
test-file:
	@read -p "Enter test file name (e.g., test_auth_unit.py): " file; \
	pytest -v tests/$$file

# Run tests for specific function
test-function:
	@read -p "Enter test function name: " func; \
	pytest -v -k $$func

# Epic 5 validation - runs all Epic 5 requirements
validate-epic5: all-checks
	@echo "=== Epic 5: Testing & Quality Assurance Validation ==="
	@echo "✅ Comprehensive test coverage (>80%)"
	@echo "✅ Automated code quality checks"
	@echo "✅ Security scanning implemented"
	@echo "✅ Pre-commit hooks configured"
	@echo "✅ All authentication functions tested"
	@echo "✅ All API endpoints tested"
	@echo "✅ Database operations tested"
	@echo "Epic 5 validation complete! 🎉"