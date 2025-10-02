SHELL := /usr/bin/bash

.PHONY: up down logs ps backend frontend db migrate makemigrations fmt lint test

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

migrate:
	cd backend && alembic upgrade head

makemigrations:
	cd backend && alembic revision --autogenerate -m "auto"

fmt:
	cd backend && ruff check --fix . && ruff format . && mypy . || true
	cd frontend && npm run lint --silent || true

lint:
	cd backend && ruff check . && mypy .
	cd frontend && npm run lint --silent

test:
	cd backend && pytest -q
