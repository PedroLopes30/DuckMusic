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

    class Config:
        pass