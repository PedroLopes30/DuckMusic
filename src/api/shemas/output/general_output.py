from pydantic import BaseModel

class DetailResponse(
    BaseModel
):
    detail : str
    
class DetailResponseWithId(
    DetailResponse
):
    
    id : int
    
class TokenResponse(
    BaseModel
):
    
    token : str