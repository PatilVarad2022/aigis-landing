#!/usr/bin/env bash
set -e

# Run migrations
python manage.py migrate --noinput

# Start Gunicorn
exec gunicorn mysite.wsgi

