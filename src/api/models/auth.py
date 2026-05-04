from sqlmodel import SQLModel , Field , Relationship
from pydantic import EmailStr
from typing import Optional

from api.core.models import BaseModel
from api.core.constants import MEDIUM_CHAR
from api.models.musics import Artist

class User(
    BaseModel,
    table=True
):
    
    photo_url : str | None = Field(
        title="User photo",
        nullable=True,
        max_length=None
    )
    
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
    
    artist : Optional[Artist] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )