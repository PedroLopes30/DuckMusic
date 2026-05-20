from pydantic import BaseModel , Field

class RegisterArtistInput(BaseModel):
    artistic_name : str = Field(
        title="artistic name",
    )
    
    biography : str | None = Field(
        title="Artistic biography"
    )

class RegisterMusicInput(BaseModel):
    name : str = Field(
        title="music name"
    )

    file_path : str = Field(
        title="file path"
    )
    
class UpdateArtistInput(BaseModel):
    artistic_name : str | None = Field(
        title="artistic name",
    )
    
    biography : str | None = Field(
        title="Artistic biography"
    )

class UpdateAlbumInput(BaseModel):
    album_name : str | None = Field(
    title="album name"),

    about : str | None = Field(
    title="about"
    )
     
    cover_url : str | None = Field(
    tittle="cover_url"
    )