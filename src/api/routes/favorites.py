from fastapi import APIRouter, status , HTTPException , Body

from api.depends.musics_dep import FavoritesMusicsRepositoryDep , MusicRepositoryDep, AlbumRepositoryDep, FavoritesAlbumsRepositoryDep
from api.depends.auth_dep import UserDep

from api.shemas.output.music_output import MusicListResponse, AlbumsListReponse
from api.shemas.output.general_output import DetailResponse

from api.models import FavoritesMusics, FavoritesAlbums

router = APIRouter(
    tags=["Favorites"],
)

@router.get(
    "/musics",
    response_model=list[MusicListResponse]
)
def get_favorite_musics(user: UserDep, repository: FavoritesMusicsRepositoryDep):
    return [favorite.musics for favorite in repository.get_by_user_id(user.id)]

@router.post(
    "/musics",
    status_code=status.HTTP_201_CREATED
)
def add_favorite_music(user: UserDep, repository: FavoritesMusicsRepositoryDep , musicRepository : MusicRepositoryDep , music_id: int = Body(embed=True)):
    if musicRepository.get_by_id(music_id) is None:
        raise HTTPException(status_code=404 , detail="music don't found")
    
    instance = FavoritesMusics(music_id=music_id ,  user_id=user.id)
    repository.create(instance)
    
    return DetailResponse(detail="favorite add")

@router.delete(
    "/musics/{music_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_favorite_music(music_id: int, user: UserDep, repository: FavoritesMusicsRepositoryDep):
    if not repository.music_exists_in_user_favorites(user.id , music_id):
        raise HTTPException(
            404 , detail="music is not in your favorites"
        )
        
    repository.delete_user_favorite_music(user.id , music_id)


@router.get(
    "/albums",
    response_model=list[AlbumsListReponse]
)
def get_favorite_albums(user: UserDep, repository: FavoritesAlbumsRepositoryDep):
    return [AlbumsListReponse(**favorite.album.model_dump() , artist=favorite.album.artist.artistic_name) for favorite in repository.get_by_user_id(user.id)]


@router.post(
    "/albums",
    status_code=status.HTTP_201_CREATED
)
def add_favorite_album(user: UserDep, repository: FavoritesAlbumsRepositoryDep, albumRepository: AlbumRepositoryDep, album_id: int = Body(embed=True)):
    if albumRepository.get_by_id(album_id) is None:
        raise HTTPException(status_code=404 , detail="album don't found")
    
    instance = FavoritesAlbums(albums_id=album_id , user_id=user.id)
    repository.create(instance)
    
    return DetailResponse(detail="favorite add")


@router.delete(
    "/albums/{album_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_favorite_album(album_id: int, user: UserDep, repository: FavoritesAlbumsRepositoryDep):
    if not repository.album_exists_in_user_favorites(user.id , album_id):
        raise HTTPException(
            404 , detail="album is not in your favorites"
        )
        
    repository.delete_user_favorite_album(user.id , album_id)