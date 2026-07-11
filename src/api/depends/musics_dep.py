from fastapi import Depends
from typing import Annotated

from api.interfaces.repository import IArtistRepository , IMusicRepository, IAlbumRepository, IPlaylistRepository
from api.repository import ArtistRepository , MusicRepository, AlbumRepository, PlaylistRepository
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

def get_playlist_repository(session: SessionDep) -> IPlaylistRepository:
    return PlaylistRepository(session)

PlaylistRepositoryDep = Annotated[IPlaylistRepository , Depends(get_playlist_repository)]