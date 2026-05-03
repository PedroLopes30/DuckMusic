from fastapi import APIRouter
from typing import Annotated

from api.shemas.input.auth_input import LoginUserSchema , RegisterUserSchema , VerifyTokenSchema , EmailUserSchema , PasswordUserSchema
from api.shemas.output.auth_output import TokenResponse
from api.shemas.output.general_output import DetailResponse , TokenResponse

router = APIRouter(
    tags=["Auth"]
)

@router.post(
    path="/login/",
    response_model=TokenResponse
)
def login_user(data : LoginUserSchema):
    pass

@router.post(
    path="/register/",
    response_model=TokenResponse,
    status_code=201,
)
def register_user(data : RegisterUserSchema):
    pass

@router.post(
    path="/token/verify/",
    status_code=204,
    tags=["token"]
)
def verify_token(data : VerifyTokenSchema):
    pass

@router.post(
    path="/reset-password/",
    status_code=200,
    response_model=TokenResponse
)
def get_reset_password_token(data : EmailUserSchema):
    pass

@router.post(
    path="/reset-password/{token}/",
    response_model=DetailResponse,
)
def reset_password(token : str , data : PasswordUserSchema):
    pass