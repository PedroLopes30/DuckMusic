from sqlmodel import SQLModel , Field
from pydantic import EmailStr

from api.core.models import BaseModel
from api.core.constants import MEDIUM_CHAR

class User(
    BaseModel,
    table=True
):
    
    name : str = Field(
        title="user name",
        min_length=1,
        nullable=False,
        index=True,
        max_length=MEDIUM_CHAR
    )
    
    email : EmailStr = Field(
        title="user email",
        max_length=MEDIUM_CHAR,
        min_length=10,
        unique=True
    )
    
    password : str = Field(
        title="user password",
        min_length=5
    )
    
    is_staff : bool = Field(
        title="user is staff",
        default=False,
    )
    