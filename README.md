## Full-Stack App (FastAPI + React)

This monorepo contains a production-grade full-stack web application:

- Backend: FastAPI, SQLAlchemy, Alembic, JWT auth, WebSockets
- Frontend: React + Vite + TypeScript
- Database: PostgreSQL
- Tooling: Docker Compose, Makefile, tests, linting, typing

### Quickstart (Docker)

1. Copy envs (defaults are fine for dev):
   - `cp backend/.env.example backend/.env`
2. Start stack:
   - `make up`
3. Open:
   - API docs: http://localhost:8000/docs
   - Frontend: http://localhost:5173

### Local Dev (without Docker)

Backend:
```
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:
```
cd frontend
npm install
npm run dev
```

### Features

- User registration and login with hashed passwords and JWT
- CRUD for Projects and Tasks
- Live Task updates via WebSocket
- Strong typing and linting, unit tests for backend

### Architecture

- `backend/`: FastAPI app with domain modules under `app/`
- `frontend/`: React app, `src/` contains features and shared libs
- `docker-compose.yml`: dev orchestration
- `Makefile`: handy commands

### Docs

- API reference: auto-generated OpenAPI at `/docs`
- See `docs/` for guides: setup, development, deployment

### License

Licensed under the MIT License. See `LICENSE`.
# yigido
Yigido's first full stack app
