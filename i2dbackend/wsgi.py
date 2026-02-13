"""
WSGI config for i2dbackend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path

# Optionally load environment variables from a .env file if present
# This is a no-op if python-dotenv is not installed
try:
    from dotenv import load_dotenv  # type: ignore
    # .env is expected at the project root (one level up from this file's directory)
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except Exception:
    pass

from django.core.wsgi import get_wsgi_application

# Use DJANGO_SETTINGS_MODULE from environment if provided; fallback to prod
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'i2dbackend.settings.prod'))

application = get_wsgi_application()
