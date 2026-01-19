#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
# Use PORT environment variable if available, otherwise default to 8000
PORT=${PORT:-8000}
exec python manage.py runserver 0.0.0.0:$PORT
