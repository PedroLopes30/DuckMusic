from pydantic import BaseModel , EmailStr

class JwtTokenResponse(
    BaseModel
):
    
    accessToken : str
    refreshToken : str
    
class UserDetailReponse(
    BaseModel
):
    
    id : int
    name : str
    email : EmailStr
    photo_url : str | None