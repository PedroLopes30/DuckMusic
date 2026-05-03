from sqlmodel import select , Session 

from api.interfaces.repository import IUserRepository
from api.models.auth import User

class UserRepository(
    IUserRepository
):
    def __init__(self , session : Session):
        self.session = session
        
    def create(self , user):
        self.session.add(user)
        self.session.flush()
        return user
    
    def get_by_email(self, email):
        query = select(User).where(User.email == email)
        return self.session.exec(query).first()