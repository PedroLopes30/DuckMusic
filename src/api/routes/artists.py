from fastapi import APIRouter

from api.shemas.input.music_input import RegisterArtistInput
from api.shemas.output.general_output import DetailResponse

from api.depends.auth_dep import UserDep

router = APIRouter(
    tags=["Artist"]
)

@router.post(
    path="/register/",
    #response_class=DetailResponse,
    status_code=201,
)
def register_artist(user : UserDep ,data : RegisterArtistInput):
    pass