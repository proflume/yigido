from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers import auth as auth_router
from app.routers import projects as projects_router
from app.routers import tasks as tasks_router
from app.routers import ws as ws_router


def create_app() -> FastAPI:
    application = FastAPI(title="Full Stack App", version="0.1.0")

    # CORS
    origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create tables automatically in dev
    if settings.ENVIRONMENT != "production":
        Base.metadata.create_all(bind=engine)

    # Routers
    application.include_router(auth_router.router, prefix="/auth", tags=["auth"])
    application.include_router(projects_router.router, prefix="/projects", tags=["projects"])
    application.include_router(tasks_router.router, prefix="/tasks", tags=["tasks"])
    application.include_router(ws_router.router)

    @application.get("/")
    def read_root():
        return {"status": "ok", "app": application.title, "version": application.version}

    return application


app = create_app()
