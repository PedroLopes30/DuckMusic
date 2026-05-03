from abc import ABC , abstractmethod

class ITokensService(
    ABC
):
    
    @abstractmethod
    def store_reset_pass_token(self, token , user_id)->None:
        pass
    
    def get_user_id_by_reset_pass_token(self,token : str)->int:
        pass
    
    @abstractmethod
    def delete_user_reset_pass_index(self , user_id : int)->None:
        pass
    
    @abstractmethod
    def delete_reset_pass_token(self , token : str) -> None:
        pass
    
    @abstractmethod
    def get_user_reset_pass_by_index(self , user_id)->str | None:
        pass
    
    @abstractmethod
    def delete_token(self , token : str)->None:
        pass
    
    @abstractmethod
    def add_token(self , token : str , value : str , ttl : int)->None:
        pass
    
    @abstractmethod
    def get(self, name : str)->str:
        pass