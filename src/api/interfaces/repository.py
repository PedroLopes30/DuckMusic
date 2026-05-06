from abc import ABC , abstractmethod
from typing import Generic , TypeVar

from api.models import User , Artist

M = TypeVar("M")

class IRepository(
    ABC,
    Generic[M]
):
    @abstractmethod
    def create(self , model : M)->M:
        pass
    
    @abstractmethod
    def get_by_id(self , id : int) -> M | None:
        pass
    
    @abstractmethod
    def update(self, model : M) -> None:
        pass
    
    @abstractmethod
    def delete(self , model : M)->None:
        pass
    
    @abstractmethod
    def get_all(self)->list[M]:
        pass
    
    @abstractmethod
    def get_limited(self , limit : int , started_at : int)->list[M]:
        pass

class IUserRepository(
    IRepository[User]
):
    @abstractmethod
    def get_by_email(self , email : str) -> User | None:
        pass
    
class IArtistRepository(
    IRepository[Artist]
):
    pass