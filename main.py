import uvicorn
from fastapi import FastAPI
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from src.testgate.auth.views import router as auth_router
from src.testgate.user.views import router as user_router
from src.testgate.role.views import router as role_router
from src.testgate.permission.views import router as permission_router
from src.testgate.repository.views import router as repository_router
from src.testgate.execution.views import router as execution_router
from src.testgate.suite.views import router as suite_router
from src.testgate.suite.views import router as case_router
from src.testgate.database.database import run_db_migrations, create_db_and_tables


tags_metadata = [
    {"name": "auth", "description": "Operations with auth"},
    {"name": "users", "description": "Operations with users."},
    {"name": "roles", "description": "Operations with roles."},
    {"name": "teams", "description": "Operations with teams."},
    {"name": "repository", "description": "Operations with repository"},
    {"name": "projects", "description": "Operations with projects."},
    {"name": "runs", "description": "Operations with runs"},
    {"name": "results", "description": "Operations with results"},
    {"name": "permissions", "description": "Operations with permissions"},
]

app = FastAPI()

app.version = "0.1.0"
app.title = "TestGate"
app.description = "TestGate Platform"

app.openapi_tags = tags_metadata

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(repository_router)
app.include_router(execution_router)
app.include_router(suite_router)
app.include_router(case_router)


@app.on_event("startup")
def on_startup():
    run_db_migrations()
    create_db_and_tables()


@app.on_event("shutdown")
async def on_shutdown():
    """Shutdown event for FastAPI application."""
    pass


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        f"{Path(__file__).stem}:app",
        host="127.0.0.1",
        port=5000,
        log_level="info",
        reload=True,
        workers=2,
    )
