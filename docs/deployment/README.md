# Deployment Documentation

Comprehensive deployment guide for the Defeah Marketing Backend system.

## 📁 Documentation Structure

- **[Production](./production.md)** - Production deployment procedures and configurations
- **[Staging](./staging.md)** - Staging environment setup and testing procedures
- **[Development](./development.md)** - Local development environment setup
- **[Docker](./docker.md)** - Docker containerization and orchestration
- **[Infrastructure](./infrastructure.md)** - Infrastructure as Code and cloud resources
- **[Monitoring](./monitoring.md)** - Application monitoring and observability
- **[Security](./security.md)** - Deployment security and hardening
- **[Troubleshooting](./troubleshooting.md)** - Common deployment issues and solutions

## 🚀 Deployment Overview

### Deployment Strategy

The Defeah Marketing Backend uses a **Blue-Green deployment** strategy with **rolling updates** for zero-downtime deployments:

```mermaid
graph TD
    Git[Git Repository] --> CI[CI/CD Pipeline]
    CI --> Build[Build & Test]
    Build --> Registry[Container Registry]
    Registry --> Staging[Staging Environment]
    Staging --> QA[Quality Assurance]
    QA --> Production[Production Environment]
    
    subgraph "Production Infrastructure"
        LB[Load Balancer]
        Blue[Blue Environment]
        Green[Green Environment]
        DB[(Database)]
        Redis[(Redis)]
        
        LB --> Blue
        LB -.-> Green
        Blue --> DB
        Blue --> Redis
        Green --> DB
        Green --> Redis
    end
```

### Environments

| Environment | Purpose | URL | Auto-Deploy |
|------------|---------|-----|-------------|
| **Development** | Local development | http://localhost:8080 | Manual |
| **Staging** | Integration testing | https://staging-api.defeah.com | Yes (main branch) |
| **Production** | Live system | https://api.defeah.com | Manual approval |

## 🏗️ Infrastructure Architecture

### Cloud Infrastructure

```mermaid
graph TB
    Internet[Internet] --> CDN[CloudFlare CDN]
    CDN --> WAF[Web Application Firewall]
    WAF --> LB[Load Balancer]
    
    subgraph "Application Tier"
        LB --> App1[App Instance 1]
        LB --> App2[App Instance 2]
        LB --> App3[App Instance 3]
    end
    
    subgraph "Data Tier"
        App1 --> DB_Primary[(PostgreSQL Primary)]
        App2 --> DB_Primary
        App3 --> DB_Primary
        DB_Primary --> DB_Replica[(PostgreSQL Replica)]
        
        App1 --> Redis_Primary[(Redis Primary)]
        App2 --> Redis_Primary
        App3 --> Redis_Primary
        Redis_Primary --> Redis_Replica[(Redis Replica)]
    end
    
    subgraph "External Services"
        App1 --> Instagram[Instagram API]
        App2 --> OpenAI[OpenAI API]
        App3 --> S3[AWS S3]
    end
```

### Resource Requirements

#### Production Environment
```yaml
application:
  instances: 3
  cpu: "2 cores"
  memory: "4GB"
  storage: "50GB SSD"

database:
  primary:
    cpu: "4 cores"
    memory: "16GB"
    storage: "500GB SSD"
  replica:
    cpu: "2 cores"
    memory: "8GB"
    storage: "500GB SSD"

cache:
  primary:
    cpu: "2 cores"
    memory: "8GB"
    storage: "100GB SSD"
  replica:
    cpu: "1 core"
    memory: "4GB"
    storage: "100GB SSD"

load_balancer:
  cpu: "2 cores"
  memory: "4GB"
  bandwidth: "1Gbps"
```

#### Staging Environment
```yaml
application:
  instances: 2
  cpu: "1 core"
  memory: "2GB"
  storage: "20GB SSD"

database:
  cpu: "2 cores"
  memory: "8GB"
  storage: "100GB SSD"

cache:
  cpu: "1 core"
  memory: "2GB"
  storage: "20GB SSD"
```

## 🛠️ Quick Deployment Guide

### Prerequisites

```bash
# Install required tools
curl -fsSL https://get.docker.com | sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installations
docker --version
kubectl version --client
helm version
```

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/defeah/marketing-backend.git
cd marketing-backend/backend

# Environment setup
cp .env.example .env
nano .env  # Configure environment variables

# Start services with Docker Compose
docker-compose up --build

# Verify deployment
curl http://localhost:8080/health
```

### Staging Deployment

```bash
# Deploy to staging
git push origin main  # Triggers automatic deployment

# Monitor deployment
kubectl get pods -n staging
kubectl logs -f deployment/defeah-marketing-api -n staging

# Verify staging deployment
curl https://staging-api.defeah.com/health
```

### Production Deployment

```bash
# Create production release
git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin v1.0.0

# Deploy to production (requires approval)
./scripts/deploy-production.sh v1.0.0

# Monitor deployment
kubectl get pods -n production
kubectl rollout status deployment/defeah-marketing-api -n production

# Verify production deployment
curl https://api.defeah.com/health
```

## 📦 Container Strategy

### Docker Configuration

```dockerfile
# Multi-stage production Dockerfile
FROM python:3.11-slim-bullseye as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim-bullseye

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/appuser/.local/bin:$PATH"

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Set up application directory
WORKDIR /app
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

### Docker Compose Configuration

```yaml
# docker-compose.yml for development
version: '3.8'

services:
  web:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/defeah_marketing
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=true
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./app:/app/app:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: defeah_marketing
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: defeah-network
```

## ☸️ Kubernetes Deployment

### Kubernetes Manifests

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: defeah-marketing
  labels:
    app: defeah-marketing
    environment: production

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: defeah-marketing-config
  namespace: defeah-marketing
data:
  PROJECT_NAME: "Defeah Marketing Backend"
  VERSION: "1.0.0"
  DEBUG: "false"
  LOG_LEVEL: "info"
  CORS_ORIGINS: "https://defeah.com,https://www.defeah.com,https://app.defeah.com"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: defeah-marketing-secrets
  namespace: defeah-marketing
type: Opaque
stringData:
  database-url: "postgresql://user:password@postgres:5432/defeah_marketing"
  redis-url: "redis://redis:6379/0"
  secret-key: "your-secret-key-here"
  instagram-client-id: "your-instagram-client-id"
  instagram-client-secret: "your-instagram-client-secret"
  openai-api-key: "your-openai-api-key"

---
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: defeah-marketing-api
  namespace: defeah-marketing
  labels:
    app: defeah-marketing-api
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: defeah-marketing-api
  template:
    metadata:
      labels:
        app: defeah-marketing-api
        version: v1
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: api
        image: defeah/marketing-backend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: defeah-marketing-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: defeah-marketing-secrets
              key: redis-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: defeah-marketing-secrets
              key: secret-key
        envFrom:
        - configMapRef:
            name: defeah-marketing-config
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: defeah-marketing-api
  namespace: defeah-marketing
  labels:
    app: defeah-marketing-api
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: defeah-marketing-api

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: defeah-marketing-ingress
  namespace: defeah-marketing
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - api.defeah.com
    secretName: defeah-marketing-tls
  rules:
  - host: api.defeah.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: defeah-marketing-api
            port:
              number: 80

---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: defeah-marketing-hpa
  namespace: defeah-marketing
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: defeah-marketing-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

### Helm Chart

```yaml
# helm/defeah-marketing/Chart.yaml
apiVersion: v2
name: defeah-marketing
description: Defeah Marketing Backend Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"

dependencies:
- name: postgresql
  version: "12.x.x"
  repository: "https://charts.bitnami.com/bitnami"
  condition: postgresql.enabled
- name: redis
  version: "17.x.x"
  repository: "https://charts.bitnami.com/bitnami"
  condition: redis.enabled

---
# helm/defeah-marketing/values.yaml
replicaCount: 3

image:
  repository: defeah/marketing-backend
  pullPolicy: IfNotPresent
  tag: "latest"

nameOverride: ""
fullnameOverride: ""

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: api.defeah.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: defeah-marketing-tls
      hosts:
        - api.defeah.com

resources:
  limits:
    cpu: 1000m
    memory: 2Gi
  requests:
    cpu: 250m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

# External services
postgresql:
  enabled: true
  auth:
    postgresPassword: "secure-password"
    database: "defeah_marketing"
  primary:
    persistence:
      enabled: true
      size: 50Gi

redis:
  enabled: true
  auth:
    enabled: false
  master:
    persistence:
      enabled: true
      size: 10Gi

# Application configuration
config:
  PROJECT_NAME: "Defeah Marketing Backend"
  VERSION: "1.0.0"
  DEBUG: false
  LOG_LEVEL: "info"
  CORS_ORIGINS: "https://defeah.com,https://www.defeah.com"

secrets:
  SECRET_KEY: "your-secret-key"
  INSTAGRAM_CLIENT_ID: "your-instagram-client-id"
  INSTAGRAM_CLIENT_SECRET: "your-instagram-client-secret"
  OPENAI_API_KEY: "your-openai-api-key"
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy Defeah Marketing Backend

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
        SECRET_KEY: test-secret-key
      run: |
        cd backend
        pytest tests/ -v --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: './backend'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    outputs:
      image: ${{ steps.image.outputs.image }}
      digest: ${{ steps.build.outputs.digest }}
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
    
    - name: Build and push Docker image
      id: build
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Output image
      id: image
      run: |
        echo "image=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.meta.outputs.version }}" >> $GITHUB_OUTPUT

  deploy-staging:
    if: github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBECONFIG_STAGING }}
    
    - name: Deploy to staging
      run: |
        helm upgrade --install defeah-marketing-staging ./helm/defeah-marketing \
          --namespace staging \
          --create-namespace \
          --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }} \
          --set image.tag=${{ github.sha }} \
          --set ingress.hosts[0].host=staging-api.defeah.com \
          --set config.DEBUG=true \
          --values helm/defeah-marketing/values-staging.yaml
    
    - name: Wait for deployment
      run: |
        kubectl rollout status deployment/defeah-marketing-staging -n staging --timeout=300s
    
    - name: Run smoke tests
      run: |
        sleep 30
        curl -f https://staging-api.defeah.com/health || exit 1

  deploy-production:
    if: startsWith(github.ref, 'refs/tags/v')
    needs: build
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBECONFIG_PRODUCTION }}
    
    - name: Deploy to production
      run: |
        helm upgrade --install defeah-marketing ./helm/defeah-marketing \
          --namespace production \
          --create-namespace \
          --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }} \
          --set image.tag=${{ github.ref_name }} \
          --values helm/defeah-marketing/values-production.yaml
    
    - name: Wait for deployment
      run: |
        kubectl rollout status deployment/defeah-marketing -n production --timeout=600s
    
    - name: Run production health checks
      run: |
        sleep 60
        curl -f https://api.defeah.com/health || exit 1
        curl -f https://api.defeah.com/ || exit 1
    
    - name: Notify deployment success
      if: success()
      run: |
        curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
          -H 'Content-type: application/json' \
          --data '{"text":"✅ Defeah Marketing Backend deployed successfully to production: ${{ github.ref_name }}"}'
    
    - name: Notify deployment failure
      if: failure()
      run: |
        curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
          -H 'Content-type: application/json' \
          --data '{"text":"❌ Defeah Marketing Backend deployment failed in production: ${{ github.ref_name }}"}'
```

## 📊 Monitoring and Observability

### Application Monitoring Setup

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'defeah-marketing-api'
    static_configs:
      - targets: ['defeah-marketing-api:80']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

---
# monitoring/alerts.yml
groups:
- name: defeah-marketing
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value }} errors per second"

  - alert: HighResponseTime
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High response time detected"
      description: "95th percentile response time is {{ $value }} seconds"

  - alert: DatabaseConnectionFailed
    expr: up{job="postgres"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Database connection failed"
      description: "PostgreSQL database is not responding"

  - alert: HighMemoryUsage
    expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage"
      description: "Memory usage is above 90%"
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Defeah Marketing Backend",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
            "legendFormat": "Error Rate %"
          }
        ]
      },
      {
        "title": "Database Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "pg_stat_database_numbackends",
            "legendFormat": "Active Connections"
          }
        ]
      }
    ]
  }
}
```

## 🔐 Security Considerations

### Deployment Security Checklist

- [ ] **Container Security**
  - [ ] Non-root user in containers
  - [ ] Read-only root filesystem
  - [ ] Minimal base images
  - [ ] Regular security updates

- [ ] **Network Security**
  - [ ] TLS/SSL enabled
  - [ ] Network policies configured
  - [ ] Firewall rules applied
  - [ ] VPN access for internal services

- [ ] **Secrets Management**
  - [ ] Kubernetes secrets for sensitive data
  - [ ] External secret management (HashiCorp Vault)
  - [ ] Regular secret rotation
  - [ ] No secrets in container images

- [ ] **Access Control**
  - [ ] RBAC configured
  - [ ] Service accounts with minimal permissions
  - [ ] Multi-factor authentication
  - [ ] Audit logging enabled

## 🚨 Rollback Procedures

### Automated Rollback

```bash
#!/bin/bash
# scripts/rollback.sh

set -e

NAMESPACE=${1:-production}
PREVIOUS_VERSION=${2:-$(kubectl rollout history deployment/defeah-marketing-api -n $NAMESPACE | tail -2 | head -1 | awk '{print $1}')}

echo "Rolling back deployment in namespace: $NAMESPACE"
echo "Rolling back to revision: $PREVIOUS_VERSION"

# Perform rollback
kubectl rollout undo deployment/defeah-marketing-api -n $NAMESPACE --to-revision=$PREVIOUS_VERSION

# Wait for rollback to complete
kubectl rollout status deployment/defeah-marketing-api -n $NAMESPACE --timeout=300s

# Verify rollback
echo "Verifying rollback..."
sleep 30
curl -f https://api.defeah.com/health

echo "Rollback completed successfully!"

# Send notification
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-type: application/json' \
  --data "{\"text\":\"🔄 Defeah Marketing Backend rolled back to revision $PREVIOUS_VERSION in $NAMESPACE\"}"
```

### Manual Rollback Steps

1. **Identify Target Version**
   ```bash
   kubectl rollout history deployment/defeah-marketing-api -n production
   ```

2. **Execute Rollback**
   ```bash
   kubectl rollout undo deployment/defeah-marketing-api -n production --to-revision=5
   ```

3. **Monitor Rollback**
   ```bash
   kubectl rollout status deployment/defeah-marketing-api -n production
   kubectl get pods -n production -w
   ```

4. **Verify Application Health**
   ```bash
   curl -f https://api.defeah.com/health
   curl -f https://api.defeah.com/
   ```

5. **Update DNS/Load Balancer** (if necessary)

6. **Notify Team**

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] Code reviewed and approved
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Database migrations tested
- [ ] Configuration validated
- [ ] Rollback plan prepared
- [ ] Team notified

### During Deployment

- [ ] Monitor deployment progress
- [ ] Check application logs
- [ ] Verify health endpoints
- [ ] Monitor system metrics
- [ ] Test critical functionality
- [ ] Verify external integrations

### Post-Deployment

- [ ] Run smoke tests
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify all services operational
- [ ] Update documentation
- [ ] Team notification sent
- [ ] Incident response ready

This comprehensive deployment documentation provides everything needed to deploy and maintain the Defeah Marketing Backend in various environments with proper monitoring, security, and rollback capabilities.