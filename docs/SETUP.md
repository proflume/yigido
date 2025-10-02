### Setup

Docker (recommended):

1. Copy envs: `cp backend/.env.example backend/.env`
2. Start: `make up`
3. Visit API `http://localhost:8000/docs` and Web `http://localhost:5173`

Local (no Docker):

- Backend: create venv, `pip install -r requirements.txt`, `alembic upgrade head`, `uvicorn app.main:app --reload`
- Frontend: `npm install`, `npm run dev`
