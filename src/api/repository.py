from sqlmodel import select , Session  , SQLModel
from typing import Generic , TypeVar

from api.interfaces.repository import IUserRepository
from api.models import User , Artist

M = TypeVar("M",bound=SQLModel)

class GenerictRepository(
    Generic[M]
):
    def __init__(self , session : Session , model : M):
        self.session = session
        self.model = model
    
    def create(self , model : M) -> M:
        self.session.add(model)
        self.session.flush()
        return model
    
    def get_by_id(self , id : int) -> M | None:
        return self.session.get(self.model , id)
    
    def update(self , model : M) -> None:
        self.session.add(model)
    
    def delete(self , model : M) -> None:
        self.session.delete(model)
        
    def get_all(self)->list[M]:
        query = select(self.model)
        return self.session.exec(query).all()
    
    def get_limited(self , limit : int , started_at : int)->list[M]:
        query = select(self.model).offset(started_at).limit(limit)
        return self.session.exec(query).all()

class UserRepository(
    GenerictRepository[User],
    IUserRepository,
):
    def __init__(self , session : Session):
        super().__init__(session , User)
        
    def get_by_email(self, email):
        query = select(self.model).where(self.model.email == email)
        return self.session.exec(query).first()

class ArtistRepository(
    GenerictRepository[Artist]
):
    def __init__(self , session : Session):
        super().__init__(session , Artist)