#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing Node.js dependencies..."
npm install

echo "Compiling SCSS to CSS..."
npm run sass:build

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Setting up superuser..."
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py setup_superuser \
        --username "${DJANGO_SUPERUSER_USERNAME:-admin}" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
        --password "$DJANGO_SUPERUSER_PASSWORD" \
        --noinput
fi

echo "Importing initial data..."
python manage.py import_data
