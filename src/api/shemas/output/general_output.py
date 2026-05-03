from pydantic import BaseModel

class DetailResponse(
    BaseModel
):
    detail : str
    
class TokenResponse(
    BaseModel
):
    
    token : str