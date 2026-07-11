from sqlmodel import SQLModel , Field , Relationship
from typing import Optional

from api.core.models import BaseModel
from api.core.constants import SHORT_CHAR , LONG_CHAR , MEDIUM_CHAR

class Artist(
    BaseModel,
    table=True,
):
    
    __tablename__ = "artists"
    
    user_id : int = Field(foreign_key="user.id")
    artistic_name : str = Field(
        title="user artistic name",
        nullable=False,
        max_length=SHORT_CHAR
    )
    
    biography : str | None = Field(
        title="artistic biography",
        nullable=True,
        max_length=LONG_CHAR
    )
    user : "User" = Relationship(back_populates="artist")
    albums : list["Album"] = Relationship(
        back_populates="artist"
    )

class Music(
    BaseModel,
    table=True
):
    __tablename__="musics"

   
    name : str = Field(
        title="music name",
        nullable=False,
        max_length=SHORT_CHAR
    )

    file_path : str = Field(
        nullable= False,
        max_length=LONG_CHAR
    )

    album_id : int = Field(foreign_key="albums.id")
    albums : "Album" = Relationship(back_populates="musics")
    
    favorites : list["FavoritesMusics"] = Relationship(back_populates="musics")
    
class Album(
    BaseModel,
    table=True,
):
    __tablename__ = "albums"
    
    artist_id : int = Field(foreign_key="artists.id")
    name : str = Field(
        title="album name",
        nullable=False,
        max_length=SHORT_CHAR
    )
    
    description : str | None = Field(
     title="album description",
     nullable=True,   
    )
    
    cover_url : str | None = Field(
        title="album cover url",
        nullable=True
    )
    
    artist : Artist = Relationship(
        back_populates="albums"
    )
    musics : list[Music] = Relationship(
        back_populates="albums"
    )
    
    favorites : list["FavoritesAlbums"] = Relationship(back_populates="album")
    
class FavoritesMusics(
    BaseModel,
    table=True,
):
    __tablename__ = "favorites_musics"

    user_id: int = Field(foreign_key="user.id")
    music_id: int = Field(foreign_key="musics.id")

    user: "User" = Relationship(back_populates="favorites_musics")
    musics: "Music" = Relationship(back_populates="favorites")
    

class FavoritesAlbums(
    BaseModel,
    table=True,
):
    __tablename__ = "favorites_albums"

    user_id: int = Field(foreign_key="user.id")
    albums_id: int = Field(foreign_key="albums.id")
    
    user: "User" = Relationship(back_populates="favorites_albums")
    album: "Album" = Relationship(back_populates="favorites")