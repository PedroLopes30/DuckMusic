from pydantic import BaseModel , Field

class RegisterArtistInput(BaseModel):
    artistic_name : str = Field(
        title="artistic name",
    )
    
    biography : str | None = Field(
        title="Artistic biography"
    )