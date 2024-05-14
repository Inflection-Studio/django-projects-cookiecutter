#!/bin/bash

poetry run python manage.py migrate                  # Apply database migrations

poetry run python manage.py collectstatic --noinput  # Collect static files

# Prepare log files
touch /deploy/gunicorn/logs/error.log

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn {{cookiecutter.project_slug}}.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --error-logfile=/deploy/gunicorn/logs/error.log \
    --capture-output \
    "$@"
