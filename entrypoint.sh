#!/bin/sh

set -e

echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.5
done
echo "✅ Database is ready!"

echo "📦 Applying database migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Auto-create superuser in DEBUG mode if none exists
if [ "$DEBUG" = "1" ]; then
  echo "🔎 Checking for existing superuser..."
  python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "blessingebele")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "blessmart.com@gmail.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "cynthia95")

if not User.objects.filter(is_superuser=True).exists():
    print(f"⚡ Creating default superuser ({username}/{password})...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print("✅ Superuser already exists, skipping creation.")
EOF
fi

# If arguments are provided (like `python manage.py createsuperuser`), run them directly
if [ "$#" -gt 0 ]; then
  echo "⚙️  Running custom command: $*"
  exec "$@"
else
  if [ "$DJANGO_ENV" = "production" ]; then
    echo "🚀 Starting Gunicorn (production mode)..."
    exec gunicorn online_poll_system.wsgi:application \
      --bind 0.0.0.0:8000 \
      --workers 4 \
      --threads 2 \
      --timeout 120
  else
    echo "🚀 Starting Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
  fi
fi
