#!/usr/bin/env bash
set -e

# Run migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    username = 'admin'
    email = 'pvarad2022@gmail.com'
    password = 'aigis2025admin'
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superuser created successfully!')
        print(f'Username: {username}')
        print(f'Password: {password}')
    else:
        print('Superuser username already exists')
else:
    print('Superuser already exists')
EOF

# Start Gunicorn
exec gunicorn mysite.wsgi

