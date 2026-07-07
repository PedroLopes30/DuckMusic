from fastapi import APIRouter , HTTPException, UploadFile, File ,Form

from api.models import Music
from api.depends.musics_dep import MusicRepositoryDep , AlbumRepositoryDep
from api.core.files import save_file
from api.shemas.output.music_output import MusicDetailResponse , MusicListResponse

from api.depends.auth_dep import UserDep , IsAlbumOnwer

router = APIRouter(
    tags=["Music"]
)

@router.post(
    path="/albums/{album_id}/musics/",
    status_code=201,
    response_model=MusicDetailResponse,
)
def add_music(repository : MusicRepositoryDep ,album : IsAlbumOnwer,name : str = Form() , music_file : UploadFile = File(...)):
    
    music_path = save_file(music_file,"musics/")
    
    music = repository.create(Music(albums=album,name=name,file_path=music_path))
    return MusicDetailResponse(id=music.id , name=music.name,file_path=music.file_path,album_id=music.album_id)
    

@router.delete(
    path="/albums/{album_id}/musics/{id_music}/",
    status_code=204
)
def delete_music(album : IsAlbumOnwer , id_music: int, repository: MusicRepositoryDep , album_id : int):
    
    music = repository.get_by_id_and_album_id(id=id_music,album_id=album_id)
    if not music:
        raise HTTPException(
            status_code=404, detail="the music doesn't exist"
        )
    
    repository.delete(music)

@router.patch(
    path="/albums/{album_id}/musics/{id_music}/",
)    
def update_music(album : IsAlbumOnwer ,id_music: int, album_id : int , repository: MusicRepositoryDep, name: str | None = Form(None), file: UploadFile | None = File(None)):
    data={}
    music = repository.get_by_id_and_album_id(id=id_music , album_id=album_id)
    
    if not music:
        raise HTTPException(
            status_code=404, detail="the music doesn't exist"
        )
    if name:
        data["name"] = name
    if file:
        data["file_path"] = save_file(file, "music/file")  
    for key , value in data.items() : setattr(music, key , value)
    repository.update(music)
    return MusicDetailResponse(**music.model_dump())

@router.get(
    path="/",
    tags=["index"],
    response_model=list[MusicListResponse]
)
def list_music(repository: MusicRepositoryDep, page: int = 0):
    return repository.get_limited(15 , page)

@router.get(
    path="/albums/{id_album}/musics/",
    response_model=list[MusicListResponse]
)
def list_music(repository: AlbumRepositoryDep , id_album : int, page: int = 0):
    return repository.get_musics_limited(id_album,15 , page)