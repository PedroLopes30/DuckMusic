from sqlmodel import SQLModel , Field , Relationship
from typing import Optional

from api.core.models import BaseModel
from api.core.constants import SHORT_CHAR , LONG_CHAR

class Category(
    BaseModel,
    table=True
):
    __tablename__="categories"
    name : str = Field(
        title="category name",
        nullable=False,
        max_length=SHORT_CHAR
    )

    slug : str = Field(
        title="slugs",
        nullable=False,
        max_length=LONG_CHAR
    )

class AlbunsCategory(
    BaseModel,
    table=True
):
    __tablename__="albuns category"
    category_id : int = Field(foreign_key="categories.id")
    album_id : int = Field(foreign_key="albums.id")