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
