#!/usr/bin/env sh
set -e
cd /app/backend
python manage.py migrate --noinput || true
python manage.py collectstatic --noinput || true
exec gunicorn honey_site.wsgi:application --chdir /app/backend --bind 0.0.0.0:${PORT:-8000} --workers 3 --threads 2 --timeout 60
