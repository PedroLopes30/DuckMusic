from fastapi import APIRouter , HTTPException
from api.shemas.input.music_input import UpdateAlbumInput
from api.shemas.output.music_output import AlbumsListReponse ,AlbumDetailReponse
from api.shemas.output.general_output import DetailResponse
from api.depends.musics_dep import AlbumRepositoryDep as RepositoryDep
from api.depends.musics_dep import ArtistRepositoryDep
from api.depends.auth_dep import User

router = APIRouter(
    tags=["Albums"],
)

@router.get(
    "/",
    response_model=list[AlbumsListReponse]
)
def get_albums_list(repository : RepositoryDep,page : int = 0):
    return [AlbumsListReponse(**album.model_dump() , artist=album.artist.artistic_name) for album in repository.get_limited(10,page)]

@router.get(
    "/{id}/",
    response_model=AlbumDetailReponse
)
def get_algum_detail(repository : RepositoryDep , id : int):
    album = repository.get_by_id(id)
    
    if album is None:
        raise HTTPException(
            status_code=404,
            detail="album not found"
        )
    
    return AlbumDetailReponse(**album.model_dump() , artist=album.artist.artistic_name)

@router.post(
    "/",
    status_code=201,
    response_model=DetailResponse
)
def create_album():
    pass

@router.delete(
    path="/{id}"
)
def delete_album(id_album: int, repository:RepositoryDep, user : User):
    album = repository.get_by_id(id=id_album)
    if not album:
        raise HTTPException (
            status_code=404, detail="The album doesn't exist"
        )
    artist = user.artist
    if artist is None:
        raise HTTPException(
            status_code=401, detail="Access denied: you are not authorized to make this change"
        )

    if not artist.id == album.artist_id:
        raise HTTPException(
            status_code=401, detail="Access denied: you are not authorized to make this change"
        )
    repository.delete(album)

@router.patch(
    path="/{id}"
)
def update_album(id_album: int, repository: RepositoryDep, user : User, data:UpdateAlbumInput):
    album = repository.get_by_id(id=id_album)
    data_dict = data.modeldump()
    if not album:
        raise HTTPException (
            status_code=404, detail="The album doesn't exist"
        )
    artist = user.artist
    if artist is None:
        raise HTTPException(
            status_code=401, detail="Access denied: you are not authorized to make this change"
        )
    if not artist.id == album.artist_id:
        raise HTTPException(
            status_code=401, detail="Access denied: you are not authorized to make this change"
        )
    for key , value in data_dict.items():
        if data_dict[key]:
            setattr(album , key , value)
        repository.update(album)
    return DetailResponse(detail="data updated")
