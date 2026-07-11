from fastapi import APIRouter , HTTPException, UploadFile, File ,Form , Header 
from fastapi.responses import StreamingResponse

from api.models import Music
from api.depends.musics_dep import MusicRepositoryDep , AlbumRepositoryDep
from api.core.files import save_file , get_file_chunk , get_file_size
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
def list_music(repository: MusicRepositoryDep, page: int = 0 , q : str = ""):
    return repository.get_limited(15 , page , name = q)

@router.get(
    path="/albums/{id_album}/musics/",
    response_model=list[MusicListResponse]
)
def list_music(repository: AlbumRepositoryDep , id_album : int, page: int = 0):
    return repository.get_musics_limited(id_album,15 , page)

@router.get(
    "/albums/{id_album}/musics/{id_music}/"
)
def music_detail(id_album : int , id_music : int , repository : MusicRepositoryDep):
    music = repository.get_by_id_and_album_id(id_music , id_album)
    if not music:
        raise HTTPException(status_code=404)
    return MusicDetailResponse(**music.model_dump())
@router.get(
    "/albums/{id_album}/musics/{id_music}/stream/"
)
def stream_music(id_album : int , id_music : int , repository : MusicRepositoryDep , music_range: str = Header(None)):
    music = repository.get_by_id_and_album_id(id_music , id_album)
    if not music:
        raise HTTPException(status_code=404)
    
    music_size = get_file_size(music.file_path)
    start , end , status_code = 0 , music_size-1 , 200
    if music_range:
        status_code = 206 
        range = range.replace("bytes=", "").split("-")
        start = int(range[0])
        if range[1]:
            end = int(range[1])
    
    end = min(end, music_size - 1)
    content_size = end - start + 1        
    
    headers = {
        "Content-Range": f"bytes {start}-{end}/{music_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_size),
    }
    
    media_type = "audio/mpeg" if music.file_path.endswith(".mp3") else "audio/wav"
    
    return StreamingResponse(
        get_file_chunk(music.file_path , start , end),
        status_code=status_code,
        media_type=media_type,
        headers=headers
    )