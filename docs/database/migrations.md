# Database Migrations

Comprehensive guide for managing database schema changes using Alembic for the Defeah Marketing Backend.

## Overview

Database migrations are managed using **Alembic**, the database migration tool for SQLAlchemy. This ensures controlled, versioned, and reversible database schema changes across all environments.

## Migration Strategy

### Migration Principles
1. **Always Forward**: Migrations should always move the database forward in version
2. **Reversible**: Every migration should have a downgrade path
3. **Atomic**: Each migration should be a single atomic operation
4. **Tested**: All migrations must be tested in development and staging
5. **Documented**: Complex migrations require detailed documentation

### Migration Types
- **Schema Migrations**: Table creation, column additions, index creation
- **Data Migrations**: Data transformations, bulk updates, data cleanup
- **Maintenance Migrations**: Performance optimizations, constraint additions
- **Emergency Migrations**: Critical fixes for production issues

## Setup and Configuration

### Alembic Configuration

The `alembic.ini` file contains the main configuration:

```ini
# alembic.ini
[alembic]
# Path to migration scripts
script_location = migrations

# Template for generating migration file names
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# Timezone for migration timestamps
timezone = UTC

# Database URL (will be overridden by environment variable)
sqlalchemy.url = postgresql://postgres:password@localhost:5433/defeah_marketing

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### Environment Configuration

The `migrations/env.py` file configures the migration environment:

```python
"""Alembic environment configuration."""
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.core.database import Base

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the database URL from environment
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Target metadata for autogenerate support
target_metadata = Base.metadata

# Include models for autogenerate
from app.models.user import User
from app.models.post import Post
from app.models.campaign import Campaign
from app.models.instagram_account import InstagramAccount
from app.models.instagram_token import InstagramToken
from app.models.instagram_rate_limit import InstagramRateLimit
from app.models.instagram_post import InstagramPost
from app.models.analytics_event import AnalyticsEvent
from app.models.ai_generation import AIGeneration
from app.models.media_file import MediaFile
from app.models.user_session import UserSession
from app.models.system_config import SystemConfig


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Migration Workflow

### Creating Migrations

#### 1. Auto-generate Migrations
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Add user profile fields"

# This creates a new migration file with detected changes
```

#### 2. Manual Migrations
```bash
# Create empty migration file for manual changes
alembic revision -m "Add custom index for performance"
```

#### 3. Data Migrations
```bash
# Create migration for data transformations
alembic revision -m "Migrate user preferences to new format"
```

### Migration File Structure

```python
"""Add user profile fields

Revision ID: 20240115_1430_abc123_add_user_profile_fields
Revises: 20240115_1400_def456_initial_schema
Create Date: 2024-01-15 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '20240115_1430_abc123'
down_revision = '20240115_1400_def456'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    # Add new columns
    op.add_column('users', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('avatar_url', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('timezone', sa.String(50), nullable=False, server_default='UTC'))
    
    # Add index
    op.create_index('idx_users_timezone', 'users', ['timezone'])


def downgrade() -> None:
    """Downgrade database schema."""
    # Remove index
    op.drop_index('idx_users_timezone', table_name='users')
    
    # Remove columns
    op.drop_column('users', 'timezone')
    op.drop_column('users', 'avatar_url')
    op.drop_column('users', 'bio')
```

### Running Migrations

#### Development Environment
```bash
# Check current migration status
alembic current

# Show migration history
alembic history --verbose

# Upgrade to latest migration
alembic upgrade head

# Upgrade to specific revision
alembic upgrade abc123

# Downgrade one migration
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade def456

# Show SQL without executing
alembic upgrade head --sql

# Stamp database with specific revision (without running migration)
alembic stamp head
```

#### Production Environment
```bash
# Always use explicit revision for production
alembic upgrade abc123

# Generate SQL script for manual review
alembic upgrade abc123 --sql > migration_script.sql

# Check what would be executed
alembic upgrade abc123 --sql | head -50
```

## Migration Best Practices

### Schema Changes

#### Safe Operations
```python
def upgrade() -> None:
    """Safe schema changes."""
    # Add nullable columns
    op.add_column('users', sa.Column('new_field', sa.String(100), nullable=True))
    
    # Add indexes concurrently (PostgreSQL)
    op.create_index('idx_users_new_field', 'users', ['new_field'], postgresql_concurrently=True)
    
    # Add constraints with validation disabled initially
    op.create_check_constraint(
        'ck_users_email_format',
        'users',
        "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'"
    )
```

#### Potentially Unsafe Operations
```python
def upgrade() -> None:
    """Operations requiring careful planning."""
    # Dropping columns (irreversible data loss)
    op.drop_column('users', 'old_field')
    
    # Adding NOT NULL columns to existing tables
    # Do this in multiple steps:
    
    # Step 1: Add nullable column
    op.add_column('users', sa.Column('required_field', sa.String(100), nullable=True))
    
    # Step 2: Populate with default values (separate migration)
    op.execute("UPDATE users SET required_field = 'default_value' WHERE required_field IS NULL")
    
    # Step 3: Make column NOT NULL (separate migration)
    op.alter_column('users', 'required_field', nullable=False)
```

### Data Migrations

#### Bulk Data Updates
```python
def upgrade() -> None:
    """Data migration example."""
    # Use bulk operations for better performance
    connection = op.get_bind()
    
    # Update user preferences format
    connection.execute("""
        UPDATE users 
        SET notification_preferences = jsonb_build_object(
            'email_analytics', COALESCE((notification_preferences->>'email_analytics')::boolean, true),
            'email_post_published', COALESCE((notification_preferences->>'email_post_published')::boolean, false),
            'push_engagement', COALESCE((notification_preferences->>'push_engagement')::boolean, true),
            'digest_frequency', COALESCE(notification_preferences->>'digest_frequency', 'weekly')
        )
        WHERE notification_preferences IS NOT NULL
    """)
    
    # Set default for NULL values
    connection.execute("""
        UPDATE users 
        SET notification_preferences = '{
            "email_analytics": true,
            "email_post_published": false,
            "push_engagement": true,
            "digest_frequency": "weekly"
        }'::jsonb
        WHERE notification_preferences IS NULL
    """)
```

#### Batch Processing for Large Tables
```python
def upgrade() -> None:
    """Process large tables in batches."""
    connection = op.get_bind()
    batch_size = 10000
    
    # Get total count
    result = connection.execute("SELECT COUNT(*) FROM analytics_events")
    total_records = result.scalar()
    
    # Process in batches
    for offset in range(0, total_records, batch_size):
        connection.execute(f"""
            UPDATE analytics_events 
            SET processed = true 
            WHERE id IN (
                SELECT id FROM analytics_events 
                WHERE processed = false 
                ORDER BY id 
                LIMIT {batch_size}
            )
        """)
        
        print(f"Processed {min(offset + batch_size, total_records)}/{total_records} records")
```

### Complex Migrations

#### Table Restructuring
```python
def upgrade() -> None:
    """Restructure table with data preservation."""
    # Step 1: Create new table with desired structure
    op.create_table(
        'posts_new',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(500), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('media_urls', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    
    # Step 2: Copy data with transformation
    op.execute("""
        INSERT INTO posts_new (id, user_id, title, content, media_urls, created_at, updated_at)
        SELECT 
            id,
            user_id,
            title,
            caption as content,
            ARRAY[media_url] as media_urls,
            created_at,
            updated_at
        FROM posts_old
        WHERE deleted_at IS NULL
    """)
    
    # Step 3: Drop old table and rename new one
    op.drop_table('posts_old')
    op.rename_table('posts_new', 'posts')
    
    # Step 4: Recreate indexes and constraints
    op.create_index('idx_posts_user_id', 'posts', ['user_id'])
    op.create_foreign_key('fk_posts_user_id', 'posts', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    """Reverse the restructuring."""
    # Implementation for rollback
    pass
```

## Testing Migrations

### Migration Testing Strategy

#### 1. Development Testing
```bash
# Test forward migration
alembic upgrade head

# Test backward migration
alembic downgrade -1
alembic upgrade head

# Test with sample data
python scripts/seed_test_data.py
alembic downgrade base
alembic upgrade head
python scripts/verify_data_integrity.py
```

#### 2. Integration Testing
```python
# tests/test_migrations.py
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class TestMigrations:
    
    @pytest.fixture
    def alembic_config(self):
        """Alembic configuration for testing."""
        config = Config("alembic.ini")
        config.set_main_option("sqlalchemy.url", "postgresql://test_user:test_pass@localhost/test_db")
        return config
    
    def test_migration_forward_backward(self, alembic_config):
        """Test migration forward and backward."""
        # Start from clean state
        command.downgrade(alembic_config, "base")
        
        # Apply all migrations
        command.upgrade(alembic_config, "head")
        
        # Downgrade one step
        command.downgrade(alembic_config, "-1")
        
        # Upgrade again
        command.upgrade(alembic_config, "head")
    
    def test_data_preservation(self, alembic_config):
        """Test that migrations preserve data integrity."""
        engine = create_engine(alembic_config.get_main_option("sqlalchemy.url"))
        
        # Setup initial data
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO users (email, hashed_password) VALUES ('test@example.com', 'hash')"))
            conn.commit()
        
        # Run migration
        command.upgrade(alembic_config, "head")
        
        # Verify data is preserved
        with engine.connect() as conn:
            result = conn.execute(text("SELECT email FROM users WHERE email = 'test@example.com'"))
            assert result.fetchone() is not None
```

#### 3. Performance Testing
```python
# scripts/test_migration_performance.py
import time
from alembic import command
from alembic.config import Config

def test_migration_performance():
    """Test migration performance with large dataset."""
    config = Config("alembic.ini")
    
    # Create large test dataset
    create_test_data(1000000)  # 1M records
    
    # Time the migration
    start_time = time.time()
    command.upgrade(config, "head")
    migration_time = time.time() - start_time
    
    print(f"Migration completed in {migration_time:.2f} seconds")
    
    # Verify data integrity
    verify_data_integrity()
    
    # Cleanup
    command.downgrade(config, "base")
```

## Production Migration Procedures

### Pre-Migration Checklist
1. **Backup Database**: Full backup with point-in-time recovery capability
2. **Test in Staging**: Run complete migration on staging environment
3. **Estimate Downtime**: Calculate expected migration duration
4. **Rollback Plan**: Prepare rollback procedures and scripts
5. **Monitor Resources**: Ensure sufficient disk space and memory
6. **Team Coordination**: Notify all stakeholders of maintenance window

### Migration Execution Steps

#### 1. Pre-Migration
```bash
# Create backup
pg_dump defeah_marketing > backup_$(date +%Y%m%d_%H%M%S).sql

# Check current migration status
alembic current

# Generate SQL script for review
alembic upgrade head --sql > migration_script.sql

# Review generated SQL
less migration_script.sql
```

#### 2. Execute Migration
```bash
# Apply migration with logging
alembic upgrade head 2>&1 | tee migration_$(date +%Y%m%d_%H%M%S).log

# Verify migration status
alembic current

# Check for any errors
tail -50 migration_$(date +%Y%m%d_%H%M%S).log
```

#### 3. Post-Migration Validation
```bash
# Run data integrity checks
python scripts/validate_data_integrity.py

# Check application health
curl -f http://localhost:8080/health

# Run smoke tests
python scripts/smoke_tests.py

# Monitor application logs
tail -f /var/log/defeah-marketing/app.log
```

### Rollback Procedures

#### Automatic Rollback
```bash
# Rollback to previous migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123

# Verify rollback
alembic current
```

#### Manual Rollback with Data Loss
```bash
# Restore from backup (data loss scenario)
dropdb defeah_marketing
createdb defeah_marketing
psql defeah_marketing < backup_20240115_143000.sql

# Update migration version
alembic stamp abc123
```

## Migration Monitoring

### Migration Metrics
```sql
-- Track migration execution time
CREATE TABLE migration_history (
    id SERIAL PRIMARY KEY,
    revision VARCHAR(50) NOT NULL,
    operation VARCHAR(20) NOT NULL, -- 'upgrade' or 'downgrade'
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds INTEGER,
    success BOOLEAN,
    error_message TEXT,
    executed_by VARCHAR(100)
);
```

### Monitoring Queries
```sql
-- Check for long-running migrations
SELECT 
    revision,
    operation,
    started_at,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - started_at)) as duration_seconds
FROM migration_history 
WHERE completed_at IS NULL
ORDER BY started_at DESC;

-- Migration success rate
SELECT 
    DATE_TRUNC('month', started_at) as month,
    COUNT(*) as total_migrations,
    COUNT(CASE WHEN success THEN 1 END) as successful_migrations,
    ROUND(COUNT(CASE WHEN success THEN 1 END) * 100.0 / COUNT(*), 2) as success_rate
FROM migration_history
GROUP BY DATE_TRUNC('month', started_at)
ORDER BY month DESC;
```

## Troubleshooting

### Common Issues

#### 1. Migration Conflicts
```bash
# Error: Multiple heads detected
alembic heads

# Merge branches
alembic merge abc123 def456 -m "Merge conflicting migrations"

# Resolve conflicts manually in generated merge file
```

#### 2. Database Connection Issues
```bash
# Test database connection
alembic current

# Check database URL
echo $DATABASE_URL

# Verify database exists
psql $DATABASE_URL -c "SELECT 1"
```

#### 3. Schema Drift
```bash
# Compare database schema with models
alembic revision --autogenerate -m "Fix schema drift"

# Review generated migration carefully
cat migrations/versions/latest_migration.py
```

#### 4. Failed Migrations
```bash
# Check migration status
alembic current

# Mark migration as completed (if manually fixed)
alembic stamp head

# Force migration (dangerous)
alembic upgrade head --sql | psql $DATABASE_URL
```

### Recovery Procedures

#### Corrupted Migration State
```bash
# Reset migration history
alembic stamp base

# Reapply all migrations
alembic upgrade head
```

#### Partial Migration Failure
```bash
# Check what was applied
alembic show abc123

# Complete migration manually
psql $DATABASE_URL < partial_migration_fix.sql

# Mark as completed
alembic stamp abc123
```

## Migration Scripts and Utilities

### Utility Scripts

#### Data Validation Script
```python
# scripts/validate_migrations.py
"""Validate database state after migrations."""

import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

def validate_schema():
    """Validate database schema integrity."""
    engine = create_engine(settings.DATABASE_URL)
    
    validations = [
        # Check foreign key constraints
        "SELECT COUNT(*) FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY'",
        
        # Check for orphaned records
        "SELECT COUNT(*) FROM posts p LEFT JOIN users u ON p.user_id = u.id WHERE u.id IS NULL",
        
        # Check data consistency
        "SELECT COUNT(*) FROM campaigns c WHERE c.start_date > c.end_date",
    ]
    
    with engine.connect() as conn:
        for validation in validations:
            result = conn.execute(text(validation))
            count = result.scalar()
            print(f"Validation: {validation[:50]}... Result: {count}")

if __name__ == "__main__":
    validate_schema()
```

#### Migration History Script
```python
# scripts/migration_history.py
"""Display migration history and status."""

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

def show_migration_history():
    """Show detailed migration history."""
    config = Config("alembic.ini")
    script_dir = ScriptDirectory.from_config(config)
    
    for revision in script_dir.walk_revisions():
        print(f"Revision: {revision.revision}")
        print(f"Down Revision: {revision.down_revision}")
        print(f"Description: {revision.doc}")
        print(f"Path: {revision.path}")
        print("-" * 50)

if __name__ == "__main__":
    show_migration_history()
```

This comprehensive migration guide ensures safe, reliable, and maintainable database schema evolution throughout the application lifecycle.