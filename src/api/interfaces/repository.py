from abc import ABC , abstractmethod
from typing import Generic , TypeVar

from api.models import User , Artist , Music, Album , Playlist , PlaylistMusics, FavoritesMusics , FavoritesAlbums

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
    def get_limited(self , limit : int , started_at : int , **filters)->list[M]:
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

class IMusicRepository(
    IRepository[Music]
):
    @abstractmethod
    def get_by_id_and_album_id(self , id : int , album_id : int)->Music:
        pass

class IAlbumRepository(
    IRepository[Album]
):
    @abstractmethod
    def get_musics_limited(self , id , limit : int , start_at : int) -> list[Music]:
        pass

class IPlaylistRepository(
    IRepository[Playlist]
): 
    pass   
    
class IFavoritesMusicsRepository(
    IRepository[FavoritesMusics]
):
    @abstractmethod
    def get_by_user_id(self , user_id : int) -> list[FavoritesMusics]:
        pass
    
    @abstractmethod
    def delete_user_favorite_music(self ,user_id : int , music_id : int) -> None:
        pass
    
    @abstractmethod
    def music_exists_in_user_favorites(self , user_id : int , music_id : int) -> bool:
        pass

class IFavoritesAlbumsRepository(
    IRepository[FavoritesAlbums]
):
    @abstractmethod
    def get_by_user_id(self , user_id : int) -> list[FavoritesAlbums]:
        pass
    
    @abstractmethod
    def delete_user_favorite_album(self ,user_id : int , album_id : int) -> None:
        pass
    
    @abstractmethod
    def album_exists_in_user_favorites(self , user_id : int , album_id : int) -> bool:
        pass
