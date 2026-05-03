from jwt import encode , decode
from bcrypt import checkpw , gensalt , hashpw
from datetime import timedelta , datetime , timezone

from api.interfaces import IAccessService , IHash
from api.models.auth import User

class JwtService(
    IAccessService
):
    def __init__(self,secret_key : str , algorithm , access_token_life_time : timedelta , refresh_token_life_time : timedelta):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_life_time = access_token_life_time
        self.refresh_token_life_time = refresh_token_life_time
    
    def create_user_tokens(self , user : User)->tuple[str,str]:
        now = datetime.now(timezone.utc)
        
        access_payload = self.get_access_token_payload(user , now) 
        
        refresh_content = self.get_refresh_token_payload(user , now)
        
        access_token = encode(access_payload , self.secret_key , algorithm=self.algorithm)
        refresh_token = encode(refresh_content , self.secret_key , algorithm=self.algorithm)
        return access_token, refresh_token
    
    def verify_token(self , token : str) -> bool:
        try:
            decode(token , self.secret_key , self.algorithm, options={"verify_exp": True})
            return True
        except:
            return False

    def get_access_token_payload(self , user : User , now : datetime)->dict:
        return {
            "user_id" : user.id,
            "username" : user.name,
            "iat" : now,
            "exp" : now + self.access_token_life_time
        }
    
    def get_refresh_token_payload(self , user : User , now : datetime)->dict:
        return  {
            "user_id": user.id , 
            "exp": now + self.refresh_token_life_time,
            "iat" : now , 
            "type" : "refresh"
        }
        
class BcryptHash(IHash):
    
    def encrypt(self, value):
        return hashpw(
            value.encode("utf8"),
            gensalt(10)
        ).decode("utf8")
        
    def verify(self, value, verify_value):
        return checkpw(
            verify_value.encode("utf8"),
            value.encode("utf8"),
        )