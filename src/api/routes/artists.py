from fastapi import APIRouter

from api.shemas.input.music_input import RegisterArtistInput
from api.shemas.output.general_output import DetailResponse
from api.shemas.output.music_output import ArtistListReponse , ArtistDetailResponse
from api.models import Artist

from api.depends.auth_dep import UserDep
from api.depends.musics_dep import ArtistRepositoryDep as RepositoryDep

router = APIRouter(
    tags=["Artist"]
)

@router.post(
    path="/register/",
    #response_class=DetailResponse,
    status_code=201,
)
def register_artist(user : UserDep ,data : RegisterArtistInput , repository : RepositoryDep):
    
    instance = Artist(
        user_id=user.id,
        **data.model_dump
    )
    
    return repository.create(instance)    

@router.get(
    path="/",
    response_model=list[ArtistListReponse]
)
def list_artists(repository : RepositoryDep,page : int = 0,):
    return repository.get_limited(10 , page)

@router.get(
    path="/{id}/",
    #response_model=ArtistDetailResponse
)
def get_artist_detail():
    pass

@router.patch(
    path="/{id}/",
    #response_model=DetailResponse
)
def update_artist():
    pass

@router.delete(
    path="/{id}/",
    status_code=204
)
def delete_artist():
    pass