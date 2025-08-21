# Production Deployment Guide - Visor I2D

## Overview

This guide covers the complete production deployment process for the Visor I2D backend system, including security hardening, monitoring setup, and maintenance procedures.

## Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 100GB minimum, SSD recommended
- **CPU**: 4 cores minimum, 8 cores recommended

### Software Dependencies
- Docker 20.10+
- Docker Compose 2.0+
- Git 2.25+
- SSL certificates (Let's Encrypt recommended)

## Quick Deployment

### 1. Clone Repository
```bash
git clone --recursive https://github.com/maccevedor/humboldt.git
cd humboldt
```

### 2. Environment Configuration
```bash
# Copy environment templates
cp visor-geografico-I2D-backend/.env.example visor-geografico-I2D-backend/.env
cp visor-geografico-I2D-backend/secret.json.example visor-geografico-I2D-backend/secret.json

# Edit configuration files
nano visor-geografico-I2D-backend/.env
nano visor-geografico-I2D-backend/secret.json
```

### 3. Run Deployment Script
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh production
```

## Manual Deployment Steps

### 1. Database Setup
```bash
# Start PostgreSQL with PostGIS
docker-compose up -d db

# Wait for database to be ready
docker-compose logs -f db

# Run migrations
docker-compose exec backend python manage.py migrate
```

### 2. Backend Deployment
```bash
# Build and start backend
docker-compose up -d backend

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Create superuser (optional)
docker-compose exec backend python manage.py createsuperuser
```

### 3. Frontend and Services
```bash
# Start all services
docker-compose up -d

# Verify all containers are running
docker-compose ps
```

## Security Configuration

### SSL/TLS Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d i2d.humboldt.org.co

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall Configuration
```bash
# UFW setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Environment Variables
```bash
# Production environment variables
export DJANGO_SETTINGS_MODULE=i2dbackend.settings.prod
export DEBUG=False
export SECURE_SSL_REDIRECT=True
export SESSION_COOKIE_SECURE=True
export CSRF_COOKIE_SECURE=True
```

## Health Monitoring

### Health Check Endpoints
- **Comprehensive**: `GET /health/`
- **Simple**: `GET /health/simple/`
- **Readiness**: `GET /health/ready/`
- **Liveness**: `GET /health/live/`

### Monitoring Setup
```bash
# Install monitoring tools
docker run -d --name=prometheus \
  -p 9090:9090 \
  prom/prometheus

docker run -d --name=grafana \
  -p 3000:3000 \
  grafana/grafana
```

### Log Management
```bash
# Configure log rotation
sudo nano /etc/logrotate.d/visor-i2d

# Content:
/var/log/django/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 django django
}
```

## Backup Procedures

### Automated Backup
```bash
# Database backup
docker-compose exec db pg_dump -U i2d_user i2d_db > backup_$(date +%Y%m%d).sql

# Volume backup
docker run --rm -v visor_postgres_data_restore:/data -v $(pwd):/backup alpine \
  tar czf /backup/volumes_$(date +%Y%m%d).tar.gz -C /data .
```

### Backup Script
```bash
#!/bin/bash
# /scripts/backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
docker-compose exec -T db pg_dump -U i2d_user i2d_db > "$BACKUP_DIR/db_$DATE.sql"

# Configuration backup
tar czf "$BACKUP_DIR/config_$DATE.tar.gz" \
  docker-compose.yml \
  visor-geografico-I2D-backend/.env \
  nginx/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## Performance Optimization

### Database Tuning
```sql
-- PostgreSQL configuration
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
SELECT pg_reload_conf();
```

### Docker Optimization
```yaml
# docker-compose.prod.yml
version: "3.8"
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
    restart: unless-stopped
```

### Nginx Optimization
```nginx
# nginx/nginx.conf
worker_processes auto;
worker_connections 1024;

http {
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;
    
    client_max_body_size 10M;
    keepalive_timeout 65;
}
```

## Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database status
docker-compose logs db

# Reset database connection
docker-compose restart db backend
```

#### Memory Issues
```bash
# Check memory usage
docker stats

# Increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### SSL Certificate Issues
```bash
# Renew certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

### Log Analysis
```bash
# Backend logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f db

# Nginx logs
docker-compose logs -f nginx

# System logs
journalctl -u docker -f
```

## Maintenance

### Regular Tasks
- **Daily**: Check health endpoints, review error logs
- **Weekly**: Update security patches, backup verification
- **Monthly**: Performance review, capacity planning
- **Quarterly**: Security audit, dependency updates

### Update Procedure
```bash
# 1. Create backup
./scripts/backup.sh

# 2. Pull updates
git pull origin main
git submodule update --recursive

# 3. Deploy updates
./scripts/deploy.sh production

# 4. Verify deployment
curl -f http://localhost/health/
```

### Rollback Procedure
```bash
# Rollback to previous version
./scripts/deploy.sh rollback

# Or manual rollback
docker-compose down
git checkout <previous-commit>
docker-compose up -d
```

## Security Checklist

- [ ] SSL/TLS certificates configured
- [ ] Firewall rules implemented
- [ ] Security headers enabled
- [ ] Rate limiting configured
- [ ] Input validation active
- [ ] Logging and monitoring setup
- [ ] Regular backups scheduled
- [ ] Security updates automated
- [ ] Access controls implemented
- [ ] Secrets management configured

## Support and Contacts

- **Technical Support**: contact@humboldt.org.co
- **Emergency Contact**: +57 1 320 2767
- **Documentation**: https://i2d.humboldt.org.co/docs/
- **Status Page**: https://status.humboldt.org.co
