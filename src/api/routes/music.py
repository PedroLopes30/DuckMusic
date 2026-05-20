from fastapi import APIRouter , HTTPException, UploadFile, File ,Form

from api.models import Music
from api.depends.musics_dep import MusicRepositoryDep , AlbumRepositoryDep
from api.core.files import save_file
from api.shemas.output.music_output import MusicDetailResponse

from api.depends.auth_dep import UserDep

router = APIRouter(
    tags=["Music"]
)

@router.post(
    path="/",
    status_code=201,
    response_model=MusicDetailResponse
)
def add_music(user : UserDep , repository : MusicRepositoryDep , album_repository : AlbumRepositoryDep ,name : str = Form() , album_id : int = Form() , music_file : UploadFile = File(...)):
    
    album = album_repository.get_by_id(album_id)
    artist = user.artist
    
    if not album:
        raise HTTPException(status_code=404 , detail="album not found")
    
    if  artist is None or album.artist_id != artist.id:
        raise HTTPException(status_code=401,detail="unauthorize")
    
    music_path = save_file(music_file)
    
    music = repository.create(Music(albums=album,name=name,file_path=music_path))
    return MusicDetailResponse(id=music.id , name=music.name,file_path=music.file_path,album_id=music.album_id)
    

@router.delete(
    path="/{id_music}",
    status_code=204
)
def delete_music(id_music: int, repository: MusicRepositoryDep):
    music = repository.get_by_id(id=id_music)
    if not music:
        raise HTTPException(
            status_code=404, detail="the music doesn't exist"
        )
    
    repository.delete(music)

@router.patch(
    path="/{id_music}",
)    
def update_music(id_music: int, repository: MusicRepositoryDep, name: str, file_path: UploadFile = File(...)):
    data={}
    music = repository.get_by_id(id=id_music)
    if not music:
        raise HTTPException(
            status_code=404, detail="the music doesn't exist"
        )
    if name:
        data["name"] = name
    if file_path:
        data["file_path"] = save_file(file_path, "music/file")  
    for key , value in data.items() : setattr(music, key , value)
    repository.update(music)
    return MusicDetailResponse(**music.model_dump())

@router.get(
    path="/"
)
def list_music(repository: MusicRepositoryDep, page: int = 0):
    return repository.get_limited(15 , page)