from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes import auth
from api.middlewares.database_middleware import DbCommitMiddleware
from api.configs.db import create_all_tables

@asynccontextmanager
async def lifespan(app : FastAPI):
    create_all_tables()
    yield

app = FastAPI(
    title="DuckMusic",
    description="",
    version="0.0.1",
    lifespan=lifespan
)

#routes
app.include_router(
    auth.router,
    prefix="/account",
)

#middlewares
app.add_middleware(DbCommitMiddleware)