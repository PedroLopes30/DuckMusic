from fastapi import APIRouter , HTTPException , Form , UploadFile

from api.shemas.output.music_output import AlbumsListReponse ,AlbumDetailReponse
from api.shemas.output.general_output import DetailResponseWithId , DetailResponse
from api.depends.auth_dep import UserDep
from api.depends.musics_dep import AlbumRepositoryDep as RepositoryDep
from api.models.musics import Album
from api.core.files import save_file

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
    response_model=DetailResponseWithId
)
def create_album(user : UserDep , repository : RepositoryDep , name : str = Form() , description : str | None = Form(None) , cover : UploadFile = Form(None)):
    artist = user.artist
    
    if artist is None:
        raise HTTPException(
            status_code=400,
            detail="You are not an artist"
        )
        
    cover_path = save_file(cover , "albums/cover")
    instance = Album(name=name , description=description , cover_url=cover_path , artist=artist)
    album = repository.create(instance)
    return DetailResponseWithId(detail="Album created successfully" , id = album.id)

@router.delete(
    path="/{id_album}/",
    status_code=204
)
def delete_album(id_album: int, repository:RepositoryDep, user : UserDep):
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
    path="/{id_album}"
)
def update_album(id_album: int, repository: RepositoryDep, user : UserDep, name : str | None = Form(None),description : str | None = Form(None),cover : UploadFile | None = Form(None)):
    album = repository.get_by_id(id=id_album)
    data_dict = {"name" : name , "description" : description}
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
            
    if cover:
        cover_url = save_file(cover,"albums/cover")
        album.cover_url=cover_url
    
    repository.update(album)
    return DetailResponse(detail="data updated")
