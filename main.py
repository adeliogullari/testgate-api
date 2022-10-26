import uvicorn
from fastapi import Body, FastAPI, status
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from src.testgate.auth.views import user_router
from src.testgate.role.views import role_router
from src.testgate.team.views import team_router
from src.testgate.database.database import create_db_and_tables

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    }
]

app = FastAPI()

app.version = "0.1.0"
app.title = "TestGate"
app.description = "TestGate Platform"

app.openapi_tags = tags_metadata

app.include_router(user_router)
app.include_router(role_router)
app.include_router(team_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

# app.add_middleware(TrustedHostMiddleware)
# app.add_middleware(HTTPSRedirectMiddleware)


# @app.get("/")
# async def root():
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Hello World"})

if __name__ == "__main__":
    uvicorn.run(f"{Path(__file__).stem}:app", host="127.0.0.1", port=5000, log_level="info", reload=True, workers=2)
