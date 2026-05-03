from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from sqladmin import Admin

from api.routes import auth
from api.middlewares.database_middleware import DbCommitMiddleware
from api.configs.db import create_all_tables , get_engine
from api.admin.auth_admin import UserAdmin
from api.admin.autenticate import authentication_backend
from api.configs.settings import settings

@asynccontextmanager
async def lifespan(app : FastAPI):
    create_all_tables()
    yield

app = FastAPI(
    title="DuckMusic",
    description="",
    version="1.0.0",
    lifespan=lifespan
)

admin = Admin(
    app,
    get_engine(),
    authentication_backend=authentication_backend
)

#routes
app.include_router(
    auth.router,
    prefix="/account",
)

#middlewares
app.add_middleware(DbCommitMiddleware)

#admin
admin.add_view(UserAdmin)

#others
if settings.DEBUG:
    app.mount("/media/",StaticFiles(directory=settings.UPLOAD_DIR),name="media")