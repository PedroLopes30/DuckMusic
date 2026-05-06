from pydantic import BaseModel

class ArtistListReponse(
    BaseModel  
):
    id : int
    artistic_name : str

class ArtistDetailResponse(
    ArtistListReponse
):
    name : str
    biography : str | None

class MusicListResponse(
    BaseModel
):
    id : int
    name : str

class MusicDetailResponse(
    MusicListResponse
):
    file_path : str
    album_id : int     
