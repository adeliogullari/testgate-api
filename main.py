import asyncio
import uvicorn
from fastapi import FastAPI
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from src.testgate.auth.views import router as auth_router
from src.testgate.suite.views import router as case_router
from src.testgate.email.views import router as email_router
from src.testgate.execution.views import router as execution_router
from src.testgate.permission.views import router as permission_router
from src.testgate.repository.views import router as repository_router
from src.testgate.role.views import router as role_router
from src.testgate.suite.views import router as suite_router
from src.testgate.user.views import router as user_router

from src.testgate.database.service import run_db_migrations, create_db_and_tables
from src.testgate.email.service import aio_kafka_email_consumer

settings = Settings()

openapi_tags = [
    {"name": "auth", "description": "Operations with auth"},
    {"name": "cases", "description": "Operations with cases"},
    {"name": "emails", "description": "Operations with email"},
    {"name": "executions", "description": "Operations with executions"},
    {"name": "permissions", "description": "Operations with permissions"},
    {"name": "repositories", "description": "Operations with repositories"},
    {"name": "roles", "description": "Operations with roles"},
    {"name": "suites", "description": "Operations with suites"},
    {"name": "users", "description": "Operations with users"},
]

app = FastAPI()

app.version = "0.1.0"
app.title = "TestGate"
app.description = "TestGate Platform"

app.openapi_tags = openapi_tags

app.include_router(auth_router)
app.include_router(case_router)
app.include_router(email_router)
app.include_router(execution_router)
app.include_router(permission_router)
app.include_router(repository_router)
app.include_router(role_router)
app.include_router(suite_router)
app.include_router(user_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Startup event for FastAPI application."""
    run_db_migrations()
    create_db_and_tables()
    asyncio.create_task(aio_kafka_email_consumer())


@app.on_event("shutdown")
def on_shutdown() -> None:
    """Shutdown event for FastAPI application."""
    pass


if __name__ == "__main__":
    uvicorn.run(
        f"{Path(__file__).stem}:app",
        host=settings.testgate_uvicorn_host,
        port=settings.testgate_uvicorn_port,
        log_level=settings.testgate_uvicorn_log_level,
        reload=settings.testgate_uvicorn_reload,
        workers=settings.testgate_uvicorn_workers,
    )
