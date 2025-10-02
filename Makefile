.PHONY: help install dev build test clean docker-up docker-down migrate

help:
	@echo "TaskFlow - Make Commands"
	@echo ""
	@echo "install          Install all dependencies"
	@echo "dev              Start development servers"
	@echo "build            Build for production"
	@echo "test             Run all tests"
	@echo "test-backend     Run backend tests"
	@echo "test-frontend    Run frontend tests"
	@echo "clean            Clean build artifacts"
	@echo "docker-up        Start Docker containers"
	@echo "docker-down      Stop Docker containers"
	@echo "migrate          Run database migrations"
	@echo "lint             Run linters"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Done!"

dev:
	@echo "Starting development servers..."
	@echo "Backend will run on http://localhost:5000"
	@echo "Frontend will run on http://localhost:3000"
	@make -j2 dev-backend dev-frontend

dev-backend:
	cd backend && python wsgi.py

dev-frontend:
	cd frontend && npm run dev

build:
	@echo "Building for production..."
	cd frontend && npm run build
	@echo "Build complete!"

test:
	@make test-backend
	@make test-frontend

test-backend:
	@echo "Running backend tests..."
	cd backend && pytest --cov=app tests/

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm test

clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/__pycache__
	rm -rf backend/**/__pycache__
	rm -rf backend/.pytest_cache
	rm -rf frontend/dist
	rm -rf frontend/node_modules/.vite
	@echo "Clean complete!"

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "Containers started!"
	@echo "Run 'make migrate' to set up the database"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down
	@echo "Containers stopped!"

migrate:
	@echo "Running database migrations..."
	cd backend && flask db upgrade
	@echo "Migrations complete!"

lint:
	@echo "Running linters..."
	cd backend && flake8 app/
	cd frontend && npm run lint
	@echo "Linting complete!"
