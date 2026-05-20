from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from sqladmin import Admin

from api.routes import auth , artists , albums, music
from api.middlewares.database_middleware import DbCommitMiddleware
from api.configs.db import create_all_tables , get_engine
from api.admin.auth_admin import UserAdmin
from api.admin.music_admin import ArtistAdmin , AlbumAdmin, MusicAdmin, CategoryAdmin
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
app.include_router(
    artists.router,
    prefix="/musics/artists",
)
app.include_router(
    albums.router,
    prefix="/albums"
)
app.include_router(
    music.router,
    prefix="/musics"
)

app.include_router(
    music.router,
    prefix="/musics"
)

#middlewares
app.add_middleware(DbCommitMiddleware)

#admin
admin.add_view(UserAdmin)
admin.add_view(ArtistAdmin)
admin.add_view(AlbumAdmin)
admin.add_view(MusicAdmin)
admin.add_view(CategoryAdmin)

#others
if settings.DEBUG:
    app.mount("/media/",StaticFiles(directory=settings.UPLOAD_DIR),name="media")