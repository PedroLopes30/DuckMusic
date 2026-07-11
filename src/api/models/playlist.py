from sqlmodel import SQLModel , Field , Relationship
from typing import Optional

from api.core.models import BaseModel
from api.core.constants import SHORT_CHAR , LONG_CHAR

class Playlist(
    BaseModel,
    table=True
):
    
    __tablename__ = "playlists"
    user_id : int = Field(foreign_key="user.id")
    name : str = Field(
        title="playlist name",
        nullable=False,
        max_length=SHORT_CHAR
    )

    description : str | None = Field(
     title="playlist description",
     nullable=True,   
    )

    cover_url : str | None = Field(
        title="playlist cover url",
        nullable=True
    )

class PlaylistMusics(
    BaseModel,
    table=True
):
    __tablename__="playlist musics"
    playlist_id : int = Field(foreign_key="playlists.id")
    music_id : int = Field(foreign_key="musics.id")