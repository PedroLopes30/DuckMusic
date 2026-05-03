from abc import ABC , abstractmethod


class IHash(ABC):
    
    @abstractmethod
    def encrypt(self , value : str) -> str:
        pass
    
    @abstractmethod
    def verify(self , value : str , verify_value : str) -> bool:
        pass