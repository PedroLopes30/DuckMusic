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
    album_id : int

class MusicDetailResponse(
    MusicListResponse
):
    file_path : str
    album_id : int     

class AlbumsListResponse(
    BaseModel
):
    id : int
    artist : str
    name : str
    cover_url : str | None
 
class AlbumDetailResponse(
    AlbumsListResponse
) :
   description : str | None 

class PlaylistsListResponse (
    BaseModel
):
    id : int
    name : str
    user_id : int

class PlaylistDetailReponse(
    PlaylistsListResponse
) :
   description : str | None     