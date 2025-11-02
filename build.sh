#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

# Run migrations automatically during build
python manage.py migrate --noinput

