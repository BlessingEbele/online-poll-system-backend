#!/bin/sh

echo "Waiting for database..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.5
done

echo "Database ready!"

# Always run migrations on startup
echo "Applying database migrations..."
python manage.py migrate --noinput

# If arguments are provided (like `python manage.py createsuperuser`), run them directly
if [ "$#" -gt 0 ]; then
  exec "$@"
else
  # Default behavior: start Django server (dev) or Gunicorn (prod)
  if [ "$DJANGO_ENV" = "production" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    echo "Starting Gunicorn..."
    exec gunicorn online_poll_system.wsgi:application --bind 0.0.0.0:8000 --workers 3
  else
    echo "Starting Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
  fi
fi
