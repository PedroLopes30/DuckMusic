from fastapi import Depends
from typing import Annotated

from api.interfaces.repository import IArtistRepository , IMusicRepository, IAlbumRepository , IFavoritesMusicsRepository, IFavoritesAlbumsRepository
from api.repository import ArtistRepository , MusicRepository, AlbumRepository , FavoriteMusicsRepository, FavoriteAlbumsRepository
from api.depends.data_dep import SessionDep

def get_artist_repository(session : SessionDep)->IArtistRepository:
    return ArtistRepository(session)

ArtistRepositoryDep = Annotated[IArtistRepository , Depends(get_artist_repository)]

def get_music_repository(session : SessionDep)->IMusicRepository:
    return MusicRepository(session)

MusicRepositoryDep = Annotated[IMusicRepository , Depends(get_music_repository)]

def get_album_repository(session : SessionDep) -> IAlbumRepository:
    return AlbumRepository(session)

AlbumRepositoryDep = Annotated[IAlbumRepository , Depends(get_album_repository)]

def get_favorites_musics_repository(session : SessionDep) -> IFavoritesMusicsRepository:
    return FavoriteMusicsRepository(session)

FavoritesMusicsRepositoryDep = Annotated[IFavoritesMusicsRepository , Depends(get_favorites_musics_repository)]

def get_favorites_albums_repository(session : SessionDep) -> IFavoritesAlbumsRepository:
    return FavoriteAlbumsRepository(session)

FavoritesAlbumsRepositoryDep = Annotated[IFavoritesAlbumsRepository , Depends(get_favorites_albums_repository)]
