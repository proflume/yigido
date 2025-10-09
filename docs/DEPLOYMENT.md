# Deployment Guide

Complete guide for deploying the Task Manager application to production.

## Table of Contents

1. [Production Checklist](#production-checklist)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Monitoring & Logging](#monitoring--logging)
7. [Backup & Recovery](#backup--recovery)

---

## Production Checklist

### Security

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable security headers
- [ ] Review and update dependencies

### Performance

- [ ] Enable database connection pooling
- [ ] Set up caching (Redis)
- [ ] Configure static file serving (CDN)
- [ ] Enable gzip compression
- [ ] Optimize database queries
- [ ] Set up database indexes

### Reliability

- [ ] Set up database backups
- [ ] Configure error logging
- [ ] Set up monitoring
- [ ] Configure health checks
- [ ] Set up automated backups
- [ ] Document recovery procedures

---

## Environment Setup

### 1. Production Environment Variables

Create a `.env` file in the backend directory:

```bash
# Django Settings
SECRET_KEY=your-very-long-random-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=taskmanager_prod
DB_USER=taskmanager_user
DB_PASSWORD=strong_database_password
DB_HOST=db-host.example.com
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# JWT
JWT_ACCESS_TOKEN_LIFETIME=15  # 15 minutes
JWT_REFRESH_TOKEN_LIFETIME=1440  # 24 hours

# Email (for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 2. Frontend Environment Variables

Create `.env.production` in the frontend directory:

```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api/v1
```

---

## Docker Deployment

### 1. Build Production Images

```bash
# Build backend
cd backend
docker build -t taskmanager-backend:latest .

# Build frontend
cd ../frontend
docker build -t taskmanager-frontend:latest .
```

### 2. Docker Compose Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.9'

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    image: taskmanager-backend:latest
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    env_file:
      - .env
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - db
    restart: always

  frontend:
    image: taskmanager-frontend:latest
    env_file:
      - .env.production
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - static_volume:/static:ro
      - media_volume:/media:ro
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 3. SSL/TLS Configuration

**Nginx configuration with SSL:**

```nginx
events {
    worker_connections 1024;
}

http {
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API with rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files
        location /static/ {
            alias /static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Media files
        location /media/ {
            alias /media/;
            expires 1y;
            add_header Cache-Control "public";
        }
    }
}
```

### 4. SSL Certificate Setup

**Using Let's Encrypt (Certbot):**

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificates will be at:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem

# Auto-renewal (add to crontab)
0 0 * * * certbot renew --quiet
```

---

## Cloud Deployment

### AWS Deployment

#### 1. EC2 Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/yourusername/task-manager.git
cd task-manager

# Set up environment variables
cp backend/.env.example backend/.env
# Edit .env with production values

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

#### 2. RDS (Database)

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('RDS_DB_NAME'),
        'USER': os.environ.get('RDS_USERNAME'),
        'PASSWORD': os.environ.get('RDS_PASSWORD'),
        'HOST': os.environ.get('RDS_HOSTNAME'),
        'PORT': os.environ.get('RDS_PORT'),
    }
}
```

#### 3. S3 (Static Files)

```python
# settings.py
if not DEBUG:
    # AWS S3 settings
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
    
    # Static files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### DigitalOcean Deployment

#### 1. App Platform

Create `app.yaml`:

```yaml
name: task-manager
region: nyc

databases:
  - name: db
    engine: PG
    version: "16"

services:
  - name: backend
    github:
      repo: yourusername/task-manager
      branch: main
      deploy_on_push: true
    build_command: pip install -r backend/requirements.txt
    run_command: |
      python backend/manage.py migrate
      gunicorn --chdir backend config.wsgi:application
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${db.DATABASE_URL}
      - key: SECRET_KEY
        scope: RUN_TIME
        type: SECRET

  - name: frontend
    github:
      repo: yourusername/task-manager
      branch: main
    build_command: cd frontend && npm install && npm run build
    run_command: cd frontend && npm start
    envs:
      - key: NEXT_PUBLIC_API_URL
        scope: RUN_AND_BUILD_TIME
        value: ${backend.PUBLIC_URL}/api/v1
```

Deploy:
```bash
doctl apps create --spec app.yaml
```

### Heroku Deployment

#### Backend

```bash
# Create Heroku app
heroku create taskmanager-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=taskmanager-backend.herokuapp.com

# Deploy
git subtree push --prefix backend heroku main

# Run migrations
heroku run python manage.py migrate
```

#### Frontend

```bash
# Create Vercel project
npm install -g vercel
cd frontend
vercel --prod
```

---

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Test frontend
        run: |
          cd frontend
          npm install
          npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          # Your deployment script
          ./deploy.sh
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          SERVER_HOST: ${{ secrets.SERVER_HOST }}
```

### GitLab CI/CD

Create `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - build
  - deploy

test-backend:
  stage: test
  image: python:3.11
  services:
    - postgres:16
  script:
    - cd backend
    - pip install -r requirements.txt
    - pytest

test-frontend:
  stage: test
  image: node:20
  script:
    - cd frontend
    - npm install
    - npm test

build:
  stage: build
  script:
    - docker build -t registry.gitlab.com/youruser/task-manager/backend:latest ./backend
    - docker build -t registry.gitlab.com/youruser/task-manager/frontend:latest ./frontend
    - docker push registry.gitlab.com/youruser/task-manager/backend:latest
    - docker push registry.gitlab.com/youruser/task-manager/frontend:latest
  only:
    - main

deploy:
  stage: deploy
  script:
    - ssh user@server "cd /app && docker-compose pull && docker-compose up -d"
  only:
    - main
```

---

## Monitoring & Logging

### 1. Application Monitoring (Sentry)

```python
# backend/config/settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
    environment="production",
)
```

### 2. Log Aggregation

**Using ELK Stack:**

```yaml
# docker-compose.prod.yml
services:
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_URL=http://elasticsearch:9200
```

### 3. Health Checks

```python
# backend/apps/core/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

---

## Backup & Recovery

### Database Backups

```bash
#!/bin/bash
# backup.sh

# Variables
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="taskmanager"
DB_USER="postgres"

# Create backup
pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Upload to S3
aws s3 cp $BACKUP_DIR/db_backup_$DATE.sql.gz s3://your-backup-bucket/

# Delete old backups (keep last 30 days)
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete
```

**Automate with cron:**
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

### Recovery

```bash
# Restore from backup
gunzip -c db_backup_20240101_020000.sql.gz | psql -U postgres -d taskmanager
```

---

## Performance Optimization

### 1. Database Query Optimization

```python
# Use select_related for foreign keys
tasks = Task.objects.select_related('user', 'category').all()

# Use prefetch_related for reverse foreign keys
users = User.objects.prefetch_related('tasks').all()

# Use only() to fetch specific fields
tasks = Task.objects.only('title', 'status').all()
```

### 2. Caching

```python
# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def task_list(request):
    # ...
```

### 3. CDN for Static Files

```python
# Use CloudFront or CloudFlare
AWS_S3_CUSTOM_DOMAIN = 'd111111abcdef8.cloudfront.net'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
```

---

This deployment guide provides a comprehensive approach to deploying the Task Manager application in production with security, performance, and reliability in mind.
