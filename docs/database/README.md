# Database Documentation

Comprehensive database documentation for the Defeah Marketing Backend PostgreSQL database.

## 📁 Documentation Structure

- **[Schema](./schema.md)** - Complete database schema with ER diagrams
- **[Migrations](./migrations.md)** - Database migration procedures and best practices
- **[Performance](./performance.md)** - Query optimization and performance tuning
- **[Backup](./backup.md)** - Backup and recovery procedures
- **[Monitoring](./monitoring.md)** - Database monitoring and alerting
- **[Maintenance](./maintenance.md)** - Regular maintenance tasks and procedures

## 🎯 Database Overview

### Technology Stack
- **Database Engine**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 with async support
- **Migration Tool**: Alembic
- **Connection Pooling**: SQLAlchemy connection pools
- **Caching**: Redis for query and session caching

### Database Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │    │   Connection    │    │   PostgreSQL    │
│     Layer       │◄──►│      Pool       │◄──►│    Database     │
│   (FastAPI)     │    │  (SQLAlchemy)   │    │      15         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Redis       │    │     Alembic     │    │   Monitoring    │
│   (Caching)     │    │  (Migrations)   │    │   (Metrics)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Core Database Tables

### User Management
- **users** - User accounts and profiles
- **user_sessions** - User session tracking

### Instagram Integration  
- **instagram_accounts** - Connected Instagram accounts
- **instagram_tokens** - OAuth tokens and refresh data
- **instagram_rate_limits** - Rate limiting tracking

### Content Management
- **posts** - Content posts with metadata
- **campaigns** - Marketing campaigns
- **media_files** - Uploaded media assets

### AI & Analytics
- **ai_generations** - AI content generation logs
- **analytics_events** - User engagement tracking
- **performance_metrics** - Campaign performance data

## 🔧 Database Configuration

### Connection Settings
```python
# Production Configuration
DATABASE_URL = "postgresql://user:password@host:5432/defeah_marketing"

# Connection Pool Settings
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 20,
    "max_overflow": 30,
    "pool_pre_ping": True,
    "pool_recycle": 3600
}
```

### Environment-Specific Configurations

#### Development
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5433/defeah_marketing
SQLALCHEMY_ECHO=true
SQLALCHEMY_POOL_SIZE=5
```

#### Testing
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5433/defeah_marketing_test
SQLALCHEMY_ECHO=false
SQLALCHEMY_POOL_SIZE=1
```

#### Production
```bash
DATABASE_URL=postgresql://user:password@db.defeah.com:5432/defeah_marketing
SQLALCHEMY_ECHO=false
SQLALCHEMY_POOL_SIZE=20
SQLALCHEMY_MAX_OVERFLOW=30
```

## 🗄️ Data Models

### Base Model
All models inherit from a base model with common fields:

```python
class BaseModel(Base):
    __abstract__ = True
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
```

### Model Relationships
```
Users ──┐
        ├── Posts
        ├── Campaigns  
        ├── Instagram_Accounts
        └── Analytics_Events

Campaigns ──┐
            └── Posts

Instagram_Accounts ──┐
                     ├── Instagram_Tokens
                     └── Instagram_Rate_Limits

Posts ──┐
        ├── Media_Files
        └── AI_Generations
```

## 📊 Database Statistics

### Expected Data Volume (Year 1)
- **Users**: ~10,000 records
- **Posts**: ~500,000 records  
- **Analytics Events**: ~10M records
- **AI Generations**: ~100,000 records
- **Total Database Size**: ~5GB

### Growth Projections
- **Monthly User Growth**: 20%
- **Posts per User per Month**: 50
- **Analytics Events per Post**: 20
- **Database Growth Rate**: ~1GB per month

## 🔍 Query Patterns

### Common Query Types
1. **User Authentication** (High Frequency)
   - User lookup by email
   - Session validation
   - Permission checks

2. **Content Retrieval** (High Frequency)
   - Posts by user with pagination
   - Campaign posts with analytics
   - Media file associations

3. **Analytics Aggregation** (Medium Frequency)
   - Performance metrics calculation
   - Engagement rate analysis
   - Campaign ROI reporting

4. **AI Operations** (Medium Frequency)
   - Generation cost tracking
   - Usage analytics
   - Performance optimization

## 🔒 Security Considerations

### Data Protection
- **Encryption at Rest**: Database encryption enabled
- **Encryption in Transit**: SSL/TLS connections required
- **Sensitive Data**: PII fields encrypted at application level
- **Access Control**: Role-based database permissions

### Audit Trail
```sql
-- Audit log table for sensitive operations
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(20) NOT NULL,
    user_id UUID,
    old_values JSONB,
    new_values JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📈 Performance Metrics

### Target Performance
- **Query Response Time**: <100ms (95th percentile)
- **Transaction Throughput**: 1000 TPS
- **Connection Pool Utilization**: <80%
- **Database CPU**: <70%
- **Database Memory**: <80%

### Monitoring Alerts
- Slow queries (>1 second)
- High connection count (>80% pool)
- Lock timeouts
- Disk space usage (>85%)
- Replication lag (>1 second)

## 🛠️ Maintenance Tasks

### Daily
- Monitor query performance
- Check error logs
- Verify backup completion
- Review connection metrics

### Weekly
- Analyze slow query log
- Update table statistics
- Review index usage
- Check disk space trends

### Monthly
- Full database performance review
- Index optimization analysis
- Schema evolution planning
- Capacity planning update

## 🚀 Quick Start

### Local Development Setup
```bash
# Start PostgreSQL container
docker run -d \
  --name defeah-postgres \
  -e POSTGRES_DB=defeah_marketing \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5433:5432 \
  postgres:15-alpine

# Run migrations
cd backend
alembic upgrade head

# Verify setup
psql postgresql://postgres:password@localhost:5433/defeah_marketing -c "\dt"
```

### Production Deployment
```bash
# Create production database
createdb defeah_marketing

# Run migrations
alembic upgrade head

# Create indexes
psql defeah_marketing < scripts/create_indexes.sql

# Set up monitoring
psql defeah_marketing < scripts/setup_monitoring.sql
```

## 🔗 Related Documentation

- [Backend Design Document](../backend_design.md)
- [API Documentation](../api/)
- [Security Documentation](../security/)
- [Deployment Guide](../deployment/)
- [Testing Documentation](../testing/)

## 📞 Support

For database-related issues:
- Check [troubleshooting guide](./troubleshooting.md)
- Review [performance tuning](./performance.md)
- Monitor [database health](./monitoring.md)
- Contact database team via Slack #db-support