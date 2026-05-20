from sqladmin import ModelView
from api.models.category import Category, AlbunsCategory
from api.models import Artist , Album, Music 
from api.depends.auth_dep import get_bcrypt_hash

hash = get_bcrypt_hash()

class ArtistAdmin(
    ModelView , model=Artist
):
    column_list = [Artist.id , Artist.artistic_name]
    
class AlbumAdmin(
    ModelView, model=Album
):
    column_list = [Album.id , Album.name]

class MusicAdmin(
    ModelView, model=Music
):    
    column_list = [Music.id, Music.name]

class CategoryAdmin(
    ModelView, model=Category
):    
    column_list = [Category.id, Category.name]
   