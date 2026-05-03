from pydantic import BaseModel

class JwtTokenResponse(
    BaseModel
):
    
    accessToken : str
    refreshToken : str