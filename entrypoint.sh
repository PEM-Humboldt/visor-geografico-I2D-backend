#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

# Executes CMD from Dockerfile
exec "$@"