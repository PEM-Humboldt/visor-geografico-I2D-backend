# Dockerfile - Visor I2D Backend
FROM python:3.12-slim-bookworm

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/project \
    DJANGO_SETTINGS_MODULE=i2dbackend.settings.prod

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd -r django && useradd -r -g django -m -d /home/django django

WORKDIR /project

# Python dependencies
COPY requirements.txt /project/
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gevent

# Project files
COPY . /project/

# Directories and permissions
RUN mkdir -p /var/log/django /app/static /app/media && \
    chown -R django:django /project /var/log/django /app/static /app/media

USER django

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health/simple/ || exit 1

EXPOSE 8001

CMD ["gunicorn", \
     "--bind", "0.0.0.0:8001", \
     "--workers", "3", \
     "--worker-class", "gevent", \
     "--worker-connections", "1000", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--timeout", "360", \
     "--keep-alive", "2", \
     "--log-level", "info", \
     "i2dbackend.wsgi:application"]
