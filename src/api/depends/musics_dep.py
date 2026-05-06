from fastapi import Depends
from typing import Annotated

from api.interfaces.repository import IArtistRepository
from api.repository import ArtistRepository
from api.depends.data_dep import SessionDep

def get_artist_repository(session : SessionDep)->IArtistRepository:
    return ArtistRepository(session)

ArtistRepositoryDep = Annotated[IArtistRepository , Depends(get_artist_repository)]