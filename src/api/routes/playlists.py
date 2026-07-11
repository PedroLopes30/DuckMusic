from fastapi import APIRouter, File , HTTPException , Form , UploadFile

from api.shemas.output.music_output import PlaylistsListResponse , PlaylistDetailReponse
from api.shemas.output.general_output import DetailResponseWithId , DetailResponse
from api.depends.auth_dep import UserDep
from api.depends.musics_dep import PlaylistRepositoryDep as RepositoryDep
from api.models.playlist import Playlist
from api.core.files import save_file

router = APIRouter(
    tags=["Playlist"],
)

@router.get(
    "/",
    response_model=list[PlaylistsListResponse]
)

def get_playlists_list(repository : RepositoryDep,page : int = 0):
    return [PlaylistsListResponse(**playlist.model_dump()) for playlist in repository.get_limited(10,page)]

@router.get(
    "/{id}/",
    response_model=PlaylistDetailReponse
)

def get_playlist_detail(repository : RepositoryDep , id : int):
    playlist = repository.get_by_id(id)

    if playlist is None:
        raise HTTPException(
            status_code=404,
            detail="playlist not found"
        )    
    
    return PlaylistDetailReponse(**playlist.model_dump())    

@router.post(
    "/",
    status_code=201,
    response_model=DetailResponseWithId
)

def create_playlist(user : UserDep , repository : RepositoryDep , name : str = Form() , description : str | None = Form(None) , cover : UploadFile = File(None)):
    cover_path = None
    if cover:
        cover_path = save_file(cover , "playlists/cover")
    instance = Playlist(name=name , description=description , cover_url=cover_path , user=user)
    playlist = repository.create(instance)
    return DetailResponseWithId(detail="Playlist created successfully" , id=playlist.id)

@router.delete(
    path="/{id_playlist}/",
    status_code=204
)

def delete_playlist(id_playlist: int, repository:RepositoryDep, user : UserDep):
    playlist = repository.get_by_id(id=id_playlist)
    
    if not playlist:
        raise HTTPException(
            status_code=404,
            detail="playlist not found"
        )
    
    if playlist.user.id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not the owner of this playlist"
        )
    
    repository.delete(playlist)

@router.patch(
    path="/{id_playlist}/",
    response_model=DetailResponse
)    

def update_playlist(id_playlist: int, repository: RepositoryDep, user: UserDep, name: str | None = Form(None), description: str | None = Form(None), cover: UploadFile | None = File(None)):
    playlist = repository.get_by_id(id=id_playlist)
    
    if not playlist:
        raise HTTPException(
            status_code=404,
            detail="playlist not found"
        )
    
    if playlist.user.id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not the owner of this playlist"
        )
    data_dict = {"name": name, "description": description}
    for key, value in data_dict.items():
        if value is not None:
            setattr(playlist, key, value)

    if cover:
        cover_path = save_file(cover, "playlists/cover")
        playlist.cover_url = cover_path

    repository.update(playlist)
    return DetailResponse(detail="Playlist updated successfully")

