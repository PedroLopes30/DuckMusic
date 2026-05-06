from fastapi import APIRouter , HTTPException

from api.shemas.input.music_input import RegisterArtistInput , UpdateArtistInput
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
    response_model=DetailResponse,
    status_code=201,
)
def register_artist(user : UserDep ,data : RegisterArtistInput , repository : RepositoryDep):
    
    if user.artist:
        raise HTTPException(
            detail="You are already an artist"
        )
    
    instance = Artist(
        user_id=user.id,
        **data.model_dump()
    )
    
    repository.create(instance)   
    return DetailResponse(detail="Artist created") 

@router.get(
    path="/",
    response_model=list[ArtistListReponse]
)
def list_artists(repository : RepositoryDep,page : int = 0,):
    return repository.get_limited(10 , page)

@router.get(
    path="/{id}/",
    response_model=ArtistDetailResponse
)
def get_artist_detail(id : int , repository : RepositoryDep):
    artist = repository.get_by_id(id)
    if artist is None:
        raise HTTPException(
            status_code=404,
            detail="artist not found"
        )
    
    return ArtistDetailResponse(id=artist.id , artistic_name = artist.artistic_name , biography = artist.biography , name=artist.user.name)

@router.patch(
    path="/",
    response_model=DetailResponse
)
def update_artist(user : UserDep , repository : RepositoryDep , data : UpdateArtistInput):
    data_dict = data.model_dump()
    artist = user.artist
    for key , value in data_dict.items():
        if data_dict[key]:
            setattr(artist , key , value)
    repository.update(artist)
    return DetailResponse(detail="data updated")

@router.delete(
    path="/",
    status_code=204
)
def delete_artist(user : UserDep , repository : RepositoryDep):
    artist = user.artist
    if not artist:
        raise HTTPException(
            400,
            detail="You are not an artist"
        )    
    repository.delete(artist)
    