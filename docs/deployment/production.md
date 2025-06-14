# Production Deployment

Comprehensive guide for deploying the Defeah Marketing Backend to production environment.

## Production Environment Overview

### Infrastructure Specifications

```yaml
# Production Infrastructure
environment: production
region: us-east-1
availability_zones: [us-east-1a, us-east-1b, us-east-1c]

compute:
  application:
    instances: 5
    instance_type: t3.large
    cpu: 2 vCPUs
    memory: 8 GiB
    storage: 50 GB gp3 SSD
    auto_scaling:
      min: 3
      max: 20
      target_cpu: 70%
      target_memory: 80%

  database:
    primary:
      instance_type: db.r6g.xlarge
      cpu: 4 vCPUs
      memory: 32 GiB
      storage: 1000 GB gp3 SSD
      iops: 3000
      multi_az: true
    replica:
      instance_type: db.r6g.large
      cpu: 2 vCPUs
      memory: 16 GiB
      storage: 1000 GB gp3 SSD
      read_replicas: 2

  cache:
    primary:
      instance_type: cache.r6g.large
      cpu: 2 vCPUs
      memory: 13.07 GiB
      node_type: Redis 7.0
    replica:
      instances: 2
      failover: automatic

networking:
  vpc_cidr: 10.0.0.0/16
  subnets:
    public: [10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24]
    private: [10.0.10.0/24, 10.0.20.0/24, 10.0.30.0/24]
    database: [10.0.100.0/24, 10.0.200.0/24, 10.0.300.0/24]
  
  load_balancer:
    type: Application Load Balancer
    scheme: internet-facing
    ssl_certificate: ACM managed
    waf: enabled
```

## Pre-Deployment Checklist

### Infrastructure Readiness

- [ ] **VPC and Networking**
  - [ ] VPC created with proper CIDR blocks
  - [ ] Subnets configured across multiple AZs
  - [ ] Internet Gateway and NAT Gateways configured
  - [ ] Route tables properly configured
  - [ ] Security groups configured with least privilege

- [ ] **Database Setup**
  - [ ] RDS PostgreSQL instance provisioned
  - [ ] Database parameter group optimized
  - [ ] Backup retention configured (30 days)
  - [ ] Read replicas configured
  - [ ] Monitoring and alerts enabled

- [ ] **Cache Setup**
  - [ ] ElastiCache Redis cluster provisioned
  - [ ] Cluster mode enabled for high availability
  - [ ] Backup and restore configured
  - [ ] Parameter group optimized

- [ ] **Container Registry**
  - [ ] ECR repository created
  - [ ] Image scanning enabled
  - [ ] Lifecycle policies configured
  - [ ] IAM permissions configured

- [ ] **Kubernetes Cluster**
  - [ ] EKS cluster provisioned
  - [ ] Node groups configured
  - [ ] Cluster autoscaler installed
  - [ ] AWS Load Balancer Controller installed
  - [ ] CSI drivers installed

### Security Checklist

- [ ] **IAM and Permissions**
  - [ ] Service roles created with minimal permissions
  - [ ] Pod security policies configured
  - [ ] Network policies applied
  - [ ] Secrets management configured

- [ ] **SSL/TLS**
  - [ ] SSL certificates provisioned
  - [ ] Certificate auto-renewal configured
  - [ ] TLS 1.3 enforced
  - [ ] Security headers configured

- [ ] **Monitoring and Logging**
  - [ ] CloudWatch logging configured
  - [ ] Prometheus and Grafana deployed
  - [ ] AlertManager configured
  - [ ] Log aggregation setup

## Infrastructure as Code

### Terraform Configuration

```hcl
# infrastructure/terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }
  }
  
  backend "s3" {
    bucket         = "defeah-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "defeah-marketing"
      Environment = "production"
      ManagedBy   = "terraform"
    }
  }
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "defeah-marketing-prod"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.10.0/24", "10.0.20.0/24", "10.0.30.0/24"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  database_subnets = ["10.0.100.0/24", "10.0.200.0/24", "10.0.300.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  enable_dns_hostnames = true
  enable_dns_support = true
  
  tags = {
    Terraform = "true"
    Environment = "production"
  }
}

# EKS Cluster
module "eks" {
  source = "terraform-aws-modules/eks/aws"
  
  cluster_name    = "defeah-marketing-prod"
  cluster_version = "1.27"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  enable_irsa = true
  
  manage_aws_auth_configmap = true
  
  aws_auth_roles = [
    {
      rolearn  = aws_iam_role.eks_admin.arn
      username = "admin"
      groups   = ["system:masters"]
    }
  ]
  
  eks_managed_node_groups = {
    main = {
      name = "main"
      
      instance_types = ["t3.large"]
      
      min_size     = 3
      max_size     = 20
      desired_size = 5
      
      disk_size = 50
      
      labels = {
        Environment = "production"
      }
      
      update_config = {
        max_unavailable_percentage = 25
      }
    }
  }
  
  tags = {
    Environment = "production"
    Terraform   = "true"
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "main" {
  identifier = "defeah-marketing-prod"
  
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.r6g.xlarge"
  
  allocated_storage     = 1000
  max_allocated_storage = 10000
  storage_type          = "gp3"
  storage_encrypted     = true
  
  db_name  = "defeah_marketing"
  username = "postgres"
  password = random_password.db_password.result
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "Sun:04:00-Sun:05:00"
  
  multi_az               = true
  publicly_accessible    = false
  copy_tags_to_snapshot  = true
  deletion_protection    = true
  
  performance_insights_enabled = true
  monitoring_interval         = 60
  monitoring_role_arn        = aws_iam_role.rds_enhanced_monitoring.arn
  
  tags = {
    Name        = "defeah-marketing-prod"
    Environment = "production"
  }
}

# ElastiCache Redis
resource "aws_elasticache_replication_group" "main" {
  replication_group_id       = "defeah-marketing-prod"
  description                = "Redis cluster for Defeah Marketing"
  
  node_type            = "cache.r6g.large"
  port                 = 6379
  parameter_group_name = aws_elasticache_parameter_group.main.name
  
  num_cache_clusters = 3
  
  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  
  automatic_failover_enabled = true
  multi_az_enabled          = true
  
  snapshot_retention_limit = 7
  snapshot_window         = "03:00-05:00"
  
  tags = {
    Name        = "defeah-marketing-prod"
    Environment = "production"
  }
}

# Security Groups
resource "aws_security_group" "rds" {
  name_prefix = "defeah-marketing-rds"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "defeah-marketing-rds"
  }
}
```

### Kubernetes Deployment Manifests

```yaml
# k8s/production/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: defeah-marketing-prod
  labels:
    name: defeah-marketing-prod
    environment: production
    team: platform

---
# k8s/production/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: defeah-marketing-config
  namespace: defeah-marketing-prod
data:
  PROJECT_NAME: "Defeah Marketing Backend"
  VERSION: "1.0.0"
  ENVIRONMENT: "production"
  DEBUG: "false"
  LOG_LEVEL: "info"
  CORS_ORIGINS: "https://defeah.com,https://www.defeah.com,https://app.defeah.com"
  RATE_LIMIT_ENABLED: "true"
  METRICS_ENABLED: "true"
  SENTRY_ENVIRONMENT: "production"

---
# k8s/production/secrets.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: defeah-marketing-prod
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        secretRef:
          accessKeyID:
            name: aws-secret
            key: access-key-id
          secretAccessKey:
            name: aws-secret
            key: secret-access-key

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: defeah-marketing-secrets
  namespace: defeah-marketing-prod
spec:
  refreshInterval: 300s
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: defeah-marketing-secrets
    creationPolicy: Owner
  data:
    - secretKey: database-url
      remoteRef:
        key: defeah-marketing/production
        property: database_url
    - secretKey: redis-url
      remoteRef:
        key: defeah-marketing/production
        property: redis_url
    - secretKey: secret-key
      remoteRef:
        key: defeah-marketing/production
        property: secret_key
    - secretKey: instagram-client-id
      remoteRef:
        key: defeah-marketing/production
        property: instagram_client_id
    - secretKey: instagram-client-secret
      remoteRef:
        key: defeah-marketing/production
        property: instagram_client_secret
    - secretKey: openai-api-key
      remoteRef:
        key: defeah-marketing/production
        property: openai_api_key

---
# k8s/production/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: defeah-marketing-api
  namespace: defeah-marketing-prod
  labels:
    app: defeah-marketing-api
    version: v1
    environment: production
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  selector:
    matchLabels:
      app: defeah-marketing-api
  template:
    metadata:
      labels:
        app: defeah-marketing-api
        version: v1
        environment: production
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: defeah-marketing-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      
      containers:
      - name: api
        image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/defeah/marketing-backend:latest
        imagePullPolicy: Always
        
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP
        
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
        - name: INSTAGRAM_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: defeah-marketing-secrets
              key: instagram-client-id
        - name: INSTAGRAM_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: defeah-marketing-secrets
              key: instagram-client-secret
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: defeah-marketing-secrets
              key: openai-api-key
        
        envFrom:
        - configMapRef:
            name: defeah-marketing-config
        
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          successThreshold: 1
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
        
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
        
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/.cache
      
      volumes:
      - name: tmp
        emptyDir:
          sizeLimit: 1Gi
      - name: cache
        emptyDir:
          sizeLimit: 500Mi
      
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - defeah-marketing-api
              topologyKey: kubernetes.io/hostname
      
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: defeah-marketing-api

---
# k8s/production/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: defeah-marketing-api
  namespace: defeah-marketing-prod
  labels:
    app: defeah-marketing-api
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
    service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: "60"
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: defeah-marketing-api

---
# k8s/production/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: defeah-marketing-ingress
  namespace: defeah-marketing-prod
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:123456789012:certificate/abcdef12-3456-7890-abcd-ef1234567890
    alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS-1-2-2019-07
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
    alb.ingress.kubernetes.io/healthcheck-path: /health
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '30'
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
    alb.ingress.kubernetes.io/healthy-threshold-count: '2'
    alb.ingress.kubernetes.io/unhealthy-threshold-count: '3'
    alb.ingress.kubernetes.io/wafv2-acl-arn: arn:aws:wafv2:us-east-1:123456789012:global/webacl/defeah-marketing-waf/12345678-1234-1234-1234-123456789012
spec:
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
# k8s/production/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: defeah-marketing-hpa
  namespace: defeah-marketing-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: defeah-marketing-api
  minReplicas: 5
  maxReplicas: 50
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
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max

---
# k8s/production/pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: defeah-marketing-pdb
  namespace: defeah-marketing-prod
spec:
  minAvailable: 3
  selector:
    matchLabels:
      app: defeah-marketing-api

---
# k8s/production/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: defeah-marketing-network-policy
  namespace: defeah-marketing-prod
spec:
  podSelector:
    matchLabels:
      app: defeah-marketing-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 5432  # PostgreSQL
    - protocol: TCP
      port: 6379  # Redis
    - protocol: TCP
      port: 443   # HTTPS
    - protocol: TCP
      port: 53    # DNS
    - protocol: UDP
      port: 53    # DNS
```

## Deployment Process

### 1. Pre-deployment Validation

```bash
#!/bin/bash
# scripts/pre-deployment-validation.sh

set -e

echo "🔍 Starting pre-deployment validation..."

# Check infrastructure
echo "Checking AWS infrastructure..."
aws eks describe-cluster --name defeah-marketing-prod --region us-east-1
aws rds describe-db-instances --db-instance-identifier defeah-marketing-prod --region us-east-1
aws elasticache describe-replication-groups --replication-group-id defeah-marketing-prod --region us-east-1

# Check Kubernetes cluster
echo "Checking Kubernetes cluster..."
kubectl cluster-info
kubectl get nodes
kubectl get namespaces

# Verify secrets
echo "Checking secrets..."
kubectl get secrets -n defeah-marketing-prod
kubectl get configmaps -n defeah-marketing-prod

# Check monitoring
echo "Checking monitoring stack..."
kubectl get pods -n monitoring
kubectl get svc -n monitoring

# Database connectivity
echo "Testing database connectivity..."
kubectl run pg-test --rm -i --tty --image postgres:15 -- psql $DATABASE_URL -c "SELECT 1"

# Redis connectivity
echo "Testing Redis connectivity..."
kubectl run redis-test --rm -i --tty --image redis:7 -- redis-cli -u $REDIS_URL ping

echo "✅ Pre-deployment validation completed successfully"
```

### 2. Database Migration

```bash
#!/bin/bash
# scripts/production-migration.sh

set -e

echo "🗄️ Starting production database migration..."

# Backup current database
echo "Creating database backup..."
kubectl create job --from=cronjob/pg-backup manual-backup-$(date +%s) -n defeah-marketing-prod

# Wait for backup to complete
kubectl wait --for=condition=complete job/manual-backup-$(date +%s) -n defeah-marketing-prod --timeout=600s

# Run migrations
echo "Running database migrations..."
kubectl run migration-job --rm -i --tty \
  --image=123456789012.dkr.ecr.us-east-1.amazonaws.com/defeah/marketing-backend:latest \
  --env="DATABASE_URL=$DATABASE_URL" \
  --restart=Never \
  -- alembic upgrade head

echo "✅ Database migration completed successfully"
```

### 3. Blue-Green Deployment

```bash
#!/bin/bash
# scripts/blue-green-deploy.sh

set -e

NAMESPACE="defeah-marketing-prod"
IMAGE_TAG=${1:-latest}
FULL_IMAGE="123456789012.dkr.ecr.us-east-1.amazonaws.com/defeah/marketing-backend:$IMAGE_TAG"

echo "🚀 Starting blue-green deployment..."
echo "Image: $FULL_IMAGE"

# Get current deployment
CURRENT_COLOR=$(kubectl get deployment defeah-marketing-api -n $NAMESPACE -o jsonpath='{.metadata.labels.color}' || echo "blue")
NEW_COLOR=$([ "$CURRENT_COLOR" = "blue" ] && echo "green" || echo "blue")

echo "Current color: $CURRENT_COLOR"
echo "New color: $NEW_COLOR"

# Deploy new version
echo "Deploying $NEW_COLOR version..."
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: defeah-marketing-api-$NEW_COLOR
  namespace: $NAMESPACE
  labels:
    app: defeah-marketing-api
    color: $NEW_COLOR
spec:
  replicas: 5
  selector:
    matchLabels:
      app: defeah-marketing-api
      color: $NEW_COLOR
  template:
    metadata:
      labels:
        app: defeah-marketing-api
        color: $NEW_COLOR
    spec:
      # ... (same as main deployment but with new image)
      containers:
      - name: api
        image: $FULL_IMAGE
        # ... (rest of container spec)
EOF

# Wait for new deployment to be ready
echo "Waiting for $NEW_COLOR deployment to be ready..."
kubectl rollout status deployment/defeah-marketing-api-$NEW_COLOR -n $NAMESPACE --timeout=600s

# Run health checks
echo "Running health checks on $NEW_COLOR deployment..."
NEW_POD=$(kubectl get pods -n $NAMESPACE -l app=defeah-marketing-api,color=$NEW_COLOR -o jsonpath='{.items[0].metadata.name}')
kubectl exec $NEW_POD -n $NAMESPACE -- curl -f http://localhost:8080/health

# Update service to point to new deployment
echo "Switching traffic to $NEW_COLOR..."
kubectl patch service defeah-marketing-api -n $NAMESPACE -p '{"spec":{"selector":{"color":"'$NEW_COLOR'"}}}'

# Wait and monitor
echo "Monitoring new deployment..."
sleep 60

# Verify external health
curl -f https://api.defeah.com/health

# Cleanup old deployment
echo "Cleaning up $CURRENT_COLOR deployment..."
kubectl delete deployment defeah-marketing-api-$CURRENT_COLOR -n $NAMESPACE

echo "✅ Blue-green deployment completed successfully"
```

### 4. Production Deployment Script

```bash
#!/bin/bash
# scripts/deploy-production.sh

set -e

# Configuration
NAMESPACE="defeah-marketing-prod"
IMAGE_TAG=${1:-latest}
SKIP_MIGRATION=${2:-false}

echo "🚀 Starting production deployment..."
echo "Image tag: $IMAGE_TAG"
echo "Skip migration: $SKIP_MIGRATION"

# Pre-deployment checks
./scripts/pre-deployment-validation.sh

# Create deployment backup
echo "Creating deployment backup..."
kubectl create backup production-backup-$(date +%s) --include-namespaces=$NAMESPACE

# Database migration
if [ "$SKIP_MIGRATION" != "true" ]; then
  ./scripts/production-migration.sh
fi

# Deploy application
./scripts/blue-green-deploy.sh $IMAGE_TAG

# Post-deployment validation
echo "Running post-deployment validation..."
./scripts/post-deployment-validation.sh

# Update monitoring dashboards
echo "Updating monitoring dashboards..."
kubectl apply -f monitoring/production-dashboards.yaml

# Send notification
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-type: application/json' \
  --data "{\"text\":\"✅ Defeah Marketing Backend deployed successfully to production: $IMAGE_TAG\"}"

echo "🎉 Production deployment completed successfully!"
echo "Application URL: https://api.defeah.com"
echo "Monitoring: https://grafana.defeah.com"
echo "Logs: https://logs.defeah.com"
```

## Monitoring and Alerting

### Production Monitoring Configuration

```yaml
# monitoring/production-prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    environment: production

rule_files:
  - "/etc/prometheus/rules/*.yml"

scrape_configs:
  - job_name: 'defeah-marketing-api'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - defeah-marketing-prod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

---
# monitoring/production-alerts.yml
groups:
- name: defeah-marketing-critical
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 2m
    labels:
      severity: critical
      service: defeah-marketing-api
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value | humanizePercentage }} (>5%)"
      runbook_url: "https://runbooks.defeah.com/high-error-rate"

  - alert: HighResponseTime
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
      service: defeah-marketing-api
    annotations:
      summary: "High response time detected"
      description: "95th percentile response time is {{ $value }}s (>1s)"

  - alert: DatabaseConnectionFailed
    expr: up{job="postgres"} == 0
    for: 1m
    labels:
      severity: critical
      service: database
    annotations:
      summary: "Database connection failed"
      description: "PostgreSQL database is not responding"

  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
    for: 5m
    labels:
      severity: warning
      service: defeah-marketing-api
    annotations:
      summary: "Pod is crash looping"
      description: "Pod {{ $labels.pod }} is restarting frequently"

  - alert: HighMemoryUsage
    expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
    for: 10m
    labels:
      severity: warning
      service: defeah-marketing-api
    annotations:
      summary: "High memory usage"
      description: "Memory usage is {{ $value | humanizePercentage }} (>90%)"

  - alert: DiskSpaceHigh
    expr: (node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes > 0.85
    for: 10m
    labels:
      severity: warning
      service: infrastructure
    annotations:
      summary: "Disk space running low"
      description: "Disk usage is {{ $value | humanizePercentage }} (>85%)"

- name: defeah-marketing-business
  rules:
  - alert: InstagramAPIRateLimit
    expr: instagram_api_rate_limit_remaining < 10
    for: 1m
    labels:
      severity: warning
      service: instagram-integration
    annotations:
      summary: "Instagram API rate limit approaching"
      description: "Instagram API rate limit remaining: {{ $value }}"

  - alert: LowDailyActiveUsers
    expr: daily_active_users < 100
    for: 1h
    labels:
      severity: warning
      service: business-metrics
    annotations:
      summary: "Low daily active users"
      description: "Daily active users: {{ $value }} (expected >100)"

  - alert: HighAICostPerDay
    expr: daily_ai_cost_usd > 500
    for: 1h
    labels:
      severity: warning
      service: ai-costs
    annotations:
      summary: "High AI costs detected"
      description: "Daily AI cost: ${{ $value }} (>$500)"
```

### Health Check Endpoints

```python
# app/api/v1/health.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.redis import get_redis
import asyncio
import httpx
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Comprehensive readiness check"""
    checks = {}
    overall_healthy = True
    
    # Database check
    try:
        db.execute("SELECT 1")
        checks["database"] = {"status": "healthy", "response_time_ms": 0}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}
        overall_healthy = False
    
    # Redis check
    try:
        redis = get_redis()
        await redis.ping()
        checks["redis"] = {"status": "healthy", "response_time_ms": 0}
    except Exception as e:
        checks["redis"] = {"status": "unhealthy", "error": str(e)}
        overall_healthy = False
    
    # External services check
    try:
        async with httpx.AsyncClient() as client:
            # Instagram API check
            instagram_response = await client.get(
                "https://graph.instagram.com/v18.0/me",
                headers={"Authorization": f"Bearer {instagram_token}"},
                timeout=5.0
            )
            checks["instagram_api"] = {
                "status": "healthy" if instagram_response.status_code == 200 else "degraded",
                "response_time_ms": instagram_response.elapsed.total_seconds() * 1000
            }
            
            # OpenAI API check
            openai_response = await client.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {openai_token}"},
                timeout=5.0
            )
            checks["openai_api"] = {
                "status": "healthy" if openai_response.status_code == 200 else "degraded",
                "response_time_ms": openai_response.elapsed.total_seconds() * 1000
            }
    except Exception as e:
        checks["external_apis"] = {"status": "degraded", "error": str(e)}
    
    if not overall_healthy:
        raise HTTPException(status_code=503, detail="Service unhealthy")
    
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }

@router.get("/health/live")
async def liveness_check():
    """Simple liveness check"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
```

## Rollback Procedures

### Automated Rollback

```bash
#!/bin/bash
# scripts/rollback-production.sh

set -e

NAMESPACE="defeah-marketing-prod"
TARGET_REVISION=${1:-"previous"}

echo "🔄 Starting production rollback..."

# Get current deployment info
CURRENT_REVISION=$(kubectl rollout history deployment/defeah-marketing-api -n $NAMESPACE | tail -1 | awk '{print $1}')
echo "Current revision: $CURRENT_REVISION"

# Determine target revision
if [ "$TARGET_REVISION" = "previous" ]; then
    TARGET_REVISION=$((CURRENT_REVISION - 1))
fi

echo "Rolling back to revision: $TARGET_REVISION"

# Create backup of current state
kubectl create backup rollback-backup-$(date +%s) --include-namespaces=$NAMESPACE

# Perform rollback
kubectl rollout undo deployment/defeah-marketing-api -n $NAMESPACE --to-revision=$TARGET_REVISION

# Wait for rollback to complete
kubectl rollout status deployment/defeah-marketing-api -n $NAMESPACE --timeout=600s

# Verify rollback
echo "Verifying rollback..."
sleep 30

# Health checks
curl -f https://api.defeah.com/health
curl -f https://api.defeah.com/health/ready

# Monitor for 5 minutes
echo "Monitoring application for 5 minutes..."
for i in {1..10}; do
    sleep 30
    if ! curl -f https://api.defeah.com/health > /dev/null 2>&1; then
        echo "❌ Health check failed during monitoring"
        exit 1
    fi
    echo "Health check $i/10 passed"
done

echo "✅ Production rollback completed successfully"

# Send notification
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-type: application/json' \
  --data "{\"text\":\"🔄 Defeah Marketing Backend rolled back to revision $TARGET_REVISION in production\"}"
```

## Security Hardening

### Production Security Configuration

```yaml
# k8s/production/security-policy.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: defeah-marketing-psp
  namespace: defeah-marketing-prod
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'

---
# AWS WAF Configuration
resource "aws_wafv2_web_acl" "main" {
  name  = "defeah-marketing-waf"
  scope = "CLOUDFRONT"

  default_action {
    allow {}
  }

  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "RateLimitRule"
    priority = 2

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 10000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimitMetric"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "defeahMarketingWAF"
    sampled_requests_enabled   = true
  }
}
```

This comprehensive production deployment guide ensures a secure, scalable, and reliable deployment of the Defeah Marketing Backend with proper monitoring, rollback capabilities, and security hardening.