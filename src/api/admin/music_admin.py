from sqladmin import ModelView

from api.models import Artist , Album
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