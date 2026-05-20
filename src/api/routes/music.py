from fastapi import APIRouter , HTTPException, UploadFile, File
from models import Music
from api.depends.musics_dep import MusicRepositoryDep
from api.core.files import save_file
from api.shemas.output.music_output import MusicDetailResponse

router = APIRouter(
    tags=["Music"]
)

@router.post(
    path="/"
)
def add_music():
    pass

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