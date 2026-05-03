from fastapi import FastAPI

from api.routes import auth

app = FastAPI(
    title="DuckMusic",
    description="",
    version="0.0.1"
)

app.include_router(
    auth.router,
    prefix="/account",
)