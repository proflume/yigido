### Deployment Notes

- Set secure secrets in environment (`JWT_SECRET_KEY`, `DATABASE_URL`, CORS origins)
- Build images and use a production process manager/reverse proxy
- Run Alembic migrations on deploy: `alembic upgrade head`
- Configure HTTPS and HSTS at your proxy (Caddy, Nginx, Traefik)

Example env vars:

```
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg://user:pass@db:5432/app
JWT_SECRET_KEY=replace-me
CORS_ORIGINS=https://yourdomain.com
```
