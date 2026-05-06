from fastapi import Depends
from typing import Annotated

from api.interfaces.repository import IArtistRepository , IMusicRepository
from api.repository import ArtistRepository , MusicRepository
from api.depends.data_dep import SessionDep

def get_artist_repository(session : SessionDep)->IArtistRepository:
    return ArtistRepository(session)

ArtistRepositoryDep = Annotated[IArtistRepository , Depends(get_artist_repository)]

def get_music_repository(session : SessionDep)->IMusicRepository:
    return MusicRepository(session)

MusicRepositoryDep = Annotated[IMusicRepository , Depends(get_music_repository)]