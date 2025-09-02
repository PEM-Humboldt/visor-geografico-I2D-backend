# Docker Image Build Instructions - Visor I2D Backend

## 🚀 Building the Security-Updated Image

### Prerequisites
- Docker installed and running
- Access to main Humboldt project repository
- Updated requirements.txt with security patches

### Build Commands

#### 1. Build for Development/Testing
```bash
# From visor-geografico-I2D-backend directory
docker build -f Dockerfile.prod -t visor-i2d-backend:security-updated .
```

#### 2. Build for Main Humboldt Project
```bash
# Navigate to main Humboldt project
cd /home/mrueda/WWW/humboldt

# Build with proper tags for main project
docker build -f visor-geografico-I2D-backend/Dockerfile.prod \
  -t humboldt/visor-i2d-backend:latest \
  -t humboldt/visor-i2d-backend:security-$(date +%Y%m%d) \
  -t humboldt/visor-i2d-backend:django-4.2 \
  visor-geografico-I2D-backend/
```

#### 3. Build with Version Tags
```bash
# Get current commit hash for tagging
cd /home/mrueda/WWW/humboldt/visor-geografico-I2D-backend
COMMIT_HASH=$(git rev-parse --short HEAD)
cd /home/mrueda/WWW/humboldt

# Build with multiple tags
docker build -f visor-geografico-I2D-backend/Dockerfile.prod \
  -t humboldt/visor-i2d-backend:latest \
  -t humboldt/visor-i2d-backend:security-updated \
  -t humboldt/visor-i2d-backend:commit-${COMMIT_HASH} \
  -t humboldt/visor-i2d-backend:django-4.2-lts \
  visor-geografico-I2D-backend/
```

### Verification Commands

#### Test the Built Image
```bash
# Check Django version
docker run --rm humboldt/visor-i2d-backend:latest python -c "import django; print(f'Django: {django.VERSION}')"

# Run security checks
docker run --rm humboldt/visor-i2d-backend:latest python manage.py check

# Verify installed packages
docker run --rm humboldt/visor-i2d-backend:latest pip list | grep -E "(Django|requests|sqlparse)"
```

#### Run with Docker Compose
```bash
# From visor-geografico-I2D-backend directory
docker-compose up --build
```

### Image Management

#### List Built Images
```bash
docker images | grep visor-i2d-backend
```

#### Remove Old Images
```bash
# Remove old vulnerable images
docker rmi $(docker images --filter "dangling=true" -q)
```

#### Push to Registry (if needed)
```bash
# Tag for registry
docker tag humboldt/visor-i2d-backend:latest your-registry.com/humboldt/visor-i2d-backend:latest

# Push to registry
docker push your-registry.com/humboldt/visor-i2d-backend:latest
```

## 🔧 Post-Build Configuration

### Environment Variables Required
```bash
# Essential environment variables
DJANGO_SECRET_KEY=your-secure-secret-key-here
DJANGO_SETTINGS_MODULE=i2dbackend.settings.prod
DB_ENGINE=django.contrib.gis.db.backends.postgis
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432
```

### Docker Compose Override for Main Project
Create a `docker-compose.override.yml` in main Humboldt project:
```yaml
version: "3"
services:
  web:
    image: humboldt/visor-i2d-backend:latest
    environment:
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=${DB_HOST}
      - DB_PORT=${DB_PORT}
    volumes:
      - ./secrets:/app/secrets:ro  # Mount secrets securely
```

## 📋 Security Validation Checklist

After building and deploying:
- [ ] All vulnerabilities resolved (run `pip-audit` on image)
- [ ] Django 4.2.16+ installed
- [ ] requests >= 2.31.0 (CVE-2023-32681 fixed)
- [ ] No deprecated packages (unicode, old pytz)
- [ ] Application starts without errors
- [ ] API endpoints respond correctly
- [ ] Database connections work
- [ ] Static files serve properly
- [ ] Health check passes

## 🚨 Rollback Plan

If issues arise with the new image:
```bash
# Build with backup requirements
cp requirements.txt.backup requirements.txt
docker build -f Dockerfile.prod -t visor-i2d-backend:rollback .

# Update docker-compose to use rollback image
# Edit docker-compose.yml to use visor-i2d-backend:rollback
```
