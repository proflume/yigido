### API Overview

Base URL: `http://localhost:8000`

- Auth
  - POST `/auth/register` { email, password, full_name? }
  - POST `/auth/token` form { username, password } -> { access_token }

- Projects (Bearer token)
  - GET `/projects/` -> Project[]
  - POST `/projects/` { name, description? } -> Project
  - DELETE `/projects/{id}` -> { ok }

- Tasks (Bearer token)
  - GET `/tasks/` -> Task[]
  - POST `/tasks/` { project_id, title, description? } -> Task
  - PATCH `/tasks/{id}` { title?, description?, is_done? } -> Task
  - DELETE `/tasks/{id}` -> { ok }

- WebSocket
  - `ws://localhost:8000/ws/tasks` broadcasts task updates
