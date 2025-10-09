#!/bin/bash
# Backend development helper script

set -e

case "$1" in
  setup)
    echo "Setting up backend..."
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cp .env.example .env
    echo "Setup complete! Edit .env file and run './backend.sh migrate'"
    ;;
  
  migrate)
    echo "Running migrations..."
    python manage.py migrate
    ;;
  
  makemigrations)
    echo "Creating migrations..."
    python manage.py makemigrations
    ;;
  
  superuser)
    echo "Creating superuser..."
    python manage.py createsuperuser
    ;;
  
  run)
    echo "Starting development server..."
    python manage.py runserver 0.0.0.0:8000
    ;;
  
  shell)
    echo "Opening Django shell..."
    python manage.py shell
    ;;
  
  test)
    echo "Running tests..."
    pytest -v
    ;;
  
  coverage)
    echo "Running tests with coverage..."
    pytest --cov=apps --cov-report=html --cov-report=term
    echo "Coverage report generated in htmlcov/"
    ;;
  
  lint)
    echo "Running linters..."
    black --check .
    isort --check-only .
    flake8 --max-line-length=120 --exclude=migrations
    ;;
  
  format)
    echo "Formatting code..."
    black .
    isort .
    ;;
  
  *)
    echo "Usage: ./backend.sh {setup|migrate|makemigrations|superuser|run|shell|test|coverage|lint|format}"
    exit 1
    ;;
esac
