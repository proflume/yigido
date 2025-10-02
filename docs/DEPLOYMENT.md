# Deployment Guide

This guide covers deploying the TaskFlow application to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Backend Deployment](#backend-deployment)
5. [Frontend Deployment](#frontend-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Nginx Configuration](#nginx-configuration)
8. [SSL/HTTPS Setup](#ssl-https-setup)
9. [Monitoring and Logging](#monitoring-and-logging)
10. [Backup and Recovery](#backup-and-recovery)

---

## Prerequisites

- Ubuntu 22.04 LTS server (or similar)
- Root or sudo access
- Domain name pointing to your server
- Minimum 2GB RAM, 2 CPU cores
- 20GB disk space

---

## Environment Setup

### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Required Packages

```bash
# Python and build tools
sudo apt install -y python3.11 python3.11-venv python3-pip

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Redis
sudo apt install -y redis-server

# Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Nginx
sudo apt install -y nginx

# Certbot for SSL
sudo apt install -y certbot python3-certbot-nginx

# Git
sudo apt install -y git
```

---

## Database Setup

### PostgreSQL Configuration

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE fullstack_app;
CREATE USER app_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE fullstack_app TO app_user;
\q
```

### Redis Configuration

```bash
# Enable Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verify Redis is running
redis-cli ping
```

---

## Backend Deployment

### 1. Clone Repository

```bash
cd /var/www
sudo git clone <repository-url> taskflow
cd taskflow/backend
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configure Environment

```bash
nano .env
```

Add production configuration:

```env
FLASK_APP=wsgi.py
FLASK_ENV=production
SECRET_KEY=<generate-strong-secret-key>
JWT_SECRET_KEY=<generate-strong-jwt-key>
DATABASE_URL=postgresql://app_user:secure_password_here@localhost:5432/fullstack_app
REDIS_URL=redis://localhost:6379/0
UPLOAD_FOLDER=/var/www/taskflow/uploads
```

Generate secret keys:
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

### 5. Run Database Migrations

```bash
flask db upgrade
```

### 6. Create Systemd Service

```bash
sudo nano /etc/systemd/system/taskflow-backend.service
```

Add the following:

```ini
[Unit]
Description=TaskFlow Backend
After=network.target postgresql.service redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/taskflow/backend
Environment="PATH=/var/www/taskflow/backend/venv/bin"
ExecStart=/var/www/taskflow/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile /var/log/taskflow/access.log \
    --error-logfile /var/log/taskflow/error.log \
    wsgi:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 7. Create Log Directory

```bash
sudo mkdir -p /var/log/taskflow
sudo chown www-data:www-data /var/log/taskflow
```

### 8. Start Backend Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable taskflow-backend
sudo systemctl start taskflow-backend
sudo systemctl status taskflow-backend
```

---

## Frontend Deployment

### 1. Navigate to Frontend Directory

```bash
cd /var/www/taskflow/frontend
```

### 2. Configure Environment

```bash
nano .env.production
```

Add:

```env
VITE_API_URL=https://yourdomain.com/api
VITE_SOCKET_URL=https://yourdomain.com
```

### 3. Build Frontend

```bash
npm install
npm run build
```

### 4. Move Build Files

```bash
sudo mkdir -p /var/www/taskflow/frontend-build
sudo cp -r dist/* /var/www/taskflow/frontend-build/
sudo chown -R www-data:www-data /var/www/taskflow/frontend-build
```

---

## Docker Deployment

Alternative deployment using Docker:

### 1. Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Configure Environment

```bash
cd /var/www/taskflow
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit both .env files with production values
```

### 4. Deploy with Docker Compose

```bash
docker-compose -f docker-compose.yml up -d
```

### 5. Run Migrations

```bash
docker-compose exec backend flask db upgrade
```

---

## Nginx Configuration

### 1. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/taskflow
```

Add:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /var/www/taskflow/frontend-build;
        try_files $uri $uri/ /index.html;
        
        # Caching for static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # WebSocket
    location /socket.io {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;

    # File upload size
    client_max_body_size 16M;
}
```

### 2. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/taskflow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## SSL/HTTPS Setup

### 1. Obtain SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 2. Auto-renewal

Certbot automatically sets up renewal. Verify:

```bash
sudo certbot renew --dry-run
```

---

## Monitoring and Logging

### 1. Application Logs

```bash
# Backend logs
sudo journalctl -u taskflow-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Database Backup Script

Create `/var/www/taskflow/scripts/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/taskflow"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U app_user fullstack_app | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable:
```bash
chmod +x /var/www/taskflow/scripts/backup.sh
```

### 3. Automate Backups

```bash
sudo crontab -e
```

Add:
```
0 2 * * * /var/www/taskflow/scripts/backup.sh
```

### 4. Set Up Process Monitor (PM2)

For additional process monitoring:

```bash
sudo npm install -g pm2
```

---

## Performance Optimization

### 1. PostgreSQL Tuning

Edit `/etc/postgresql/16/main/postgresql.conf`:

```
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 16MB
min_wal_size = 1GB
max_wal_size = 4GB
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### 2. Redis Tuning

Edit `/etc/redis/redis.conf`:

```
maxmemory 256mb
maxmemory-policy allkeys-lru
```

Restart Redis:
```bash
sudo systemctl restart redis-server
```

---

## Security Hardening

### 1. Firewall Setup

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Fail2Ban

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Regular Updates

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Troubleshooting

### Check Service Status

```bash
sudo systemctl status taskflow-backend
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis-server
```

### View Logs

```bash
# Backend
sudo journalctl -u taskflow-backend -n 100 --no-pager

# Nginx
sudo tail -n 100 /var/log/nginx/error.log
```

### Restart Services

```bash
sudo systemctl restart taskflow-backend
sudo systemctl restart nginx
```

---

## Rollback Procedure

If deployment fails:

```bash
# Stop services
sudo systemctl stop taskflow-backend

# Restore database from backup
gunzip < /var/backups/taskflow/db_TIMESTAMP.sql.gz | psql -U app_user fullstack_app

# Revert code
cd /var/www/taskflow
git checkout <previous-commit>

# Restart services
sudo systemctl start taskflow-backend
```

---

## Support

For issues or questions, refer to the main README.md or open an issue on GitHub.
