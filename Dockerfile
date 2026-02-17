# Development Dockerfile for Visor I2D Backend - Security Updated
FROM python:3.12-slim-bookworm

# Set environment variables for development
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/project \
    DJANGO_SETTINGS_MODULE=i2dbackend.settings.local

# Install system dependencies (including dev tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /project

# Install Python dependencies
COPY requirements.txt /project/
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gevent

# Copy project files
COPY . /project/

# Create necessary directories and set permissions
RUN mkdir -p /var/log/django /project/static /project/media && \
    chmod 755 /project/static /project/media /var/log/django && \
    find /project -type f -exec chmod 644 {} \; && \
    find /project -type d -exec chmod 755 {} \; && \
    chmod +x /project/manage.py

# Expose port
EXPOSE 8001

# Development command (can be overridden in docker-compose.yml)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
