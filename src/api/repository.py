from sqlmodel import select , Session  , SQLModel
from sqlalchemy import delete
from typing import Generic , TypeVar

from api.interfaces.repository import IUserRepository
from api.models import User , Artist , Music , Album , Playlist , FavoritesMusics, FavoritesAlbums

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
    
    def get_limited(self , limit : int , started_at : int , **filters)->list[M]:
        query = select(self.model).offset(started_at).limit(limit).where(*[getattr(self.model , filter) == value for filter , value in filters.items()])
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

class MusicRepository(
    GenerictRepository[Music]
):
    
    def __init__(self, session):
        super().__init__(session, Music)
        
    def get_by_id_and_album_id(self , id : int , album_id : int)->Music:
        return self.session.exec(select(Music).where(Music.album_id == album_id , Music.id == id)).first()
    
            
class AlbumRepository(
    GenerictRepository[Album]
):
    
    def __init__(self, session: Session):
        super().__init__(session, Album)

    def get_musics_limited(self , id , limit : int , started_at : int)->list[Music]:
        query = select(Music).where(Music.album_id == id).offset(started_at).limit(limit)
        return self.session.exec(query).all()

class PlaylistRepository(
    GenerictRepository[Playlist]
):
    def __init__(self, session: Session):
        super().__init__(session, Playlist) 
 
class FavoriteMusicsRepository(
    GenerictRepository[FavoritesMusics]
):
    def __init__(self, session):
        super().__init__(session, FavoritesMusics)
        
    def get_by_user_id(self , user_id : int) -> list[FavoritesMusics]:
        query = select(FavoritesMusics).where(FavoritesMusics.user_id == user_id)
        return self.session.exec(query).all()
    
    def delete_user_favorite_music(self ,user_id : int , music_id : int) -> None:
        self.session.exec(delete(FavoritesMusics).where(FavoritesMusics.user_id == user_id , FavoritesMusics.music_id == music_id))
        
    def music_exists_in_user_favorites(self , user_id : int , music_id : int) -> bool:
        query = select(FavoritesMusics).where(FavoritesMusics.user_id == user_id ,  FavoritesMusics.music_id == music_id)
        return self.session.scalar(query) is not None

class FavoriteAlbumsRepository(
    GenerictRepository[FavoritesAlbums]
):
    def __init__(self, session):
        super().__init__(session, FavoritesAlbums)

    def get_by_user_id(self , user_id : int) -> list[FavoritesAlbums]:
        query = select(FavoritesAlbums).where(FavoritesAlbums.user_id == user_id)
        return self.session.exec(query).all()

    def delete_user_favorite_album(self , user_id : int , album_id : int) -> None:
        self.session.exec(delete(FavoritesAlbums).where(FavoritesAlbums.user_id == user_id , FavoritesAlbums.albums_id == album_id))

    def album_exists_in_user_favorites(self , user_id : int , album_id : int) -> bool:
        query = select(FavoritesAlbums).where(FavoritesAlbums.user_id == user_id ,  FavoritesAlbums.albums_id == album_id)
        return self.session.scalar(query) is not None
        
