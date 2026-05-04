from sqlmodel import select , Session  , SQLModel
from typing import Generic , TypeVar

from api.interfaces.repository import IUserRepository
from api.models import User , Artist

M = TypeVar("M",bound=SQLModel)

class GenerictRepository(
    Generic[M]
):
    def __init__(self , session : Session):
        self.session = session
    
    def create(self , model : M) -> M:
        self.session.add(model)
        self.session.flush()
        return model
    
    def get_by_id(self , model : M , id : int) -> M | None:
        return self.session.get(model , id)
    
    def update(self , model : M) -> None:
        self.session.add(model)
    
    def delete(self , model : M) -> None:
        self.delete(model)

class UserRepository(
    GenerictRepository[User],
    IUserRepository,
):
    def __init__(self , session : Session):
        self.session = session
    
    def get_by_email(self, email):
        query = select(User).where(User.email == email)
        return self.session.exec(query).first()
    
    def get_by_id(self, id):
        return self.get_by_id(User , id)

class ArtistRepository(
    GenerictRepository[Artist]
):
    def __init__(self , session : Session):
        self.session = session