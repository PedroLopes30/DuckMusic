from abc import ABC , abstractmethod

from api.models.auth import User

class IAccessService(ABC):
    @abstractmethod
    def create_user_tokens(self , user : User)->tuple[str,str]:
        pass
    
    @abstractmethod
    def verify_token(self , token : str) -> bool:
        pass
    
    @abstractmethod
    def decode(self , token) -> dict[str, str]:
        pass