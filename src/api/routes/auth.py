from fastapi import APIRouter , HTTPException

from api.shemas.input.auth_input import LoginUserSchema , RegisterUserSchema , VerifyTokenSchema , EmailUserSchema , PasswordUserSchema
from api.shemas.output.auth_output import JwtTokenResponse
from api.shemas.output.general_output import DetailResponse , TokenResponse
from api.models.auth import User

from api.depends.auth_dep import UserRepositoryDep as Repository , JwtAccessServiceDep ,BcryptHashDep

router = APIRouter(
    tags=["Auth"]
)

@router.post(
    path="/login/",
    response_model=JwtTokenResponse
)
def login_user(data : LoginUserSchema , repository : Repository , accessManager : JwtAccessServiceDep , hash :BcryptHashDep): 
    user = repository.get_by_email(data.email)
    
    if(user is None or not hash.verify(user.password,data.password)):
        raise HTTPException(
            status_code=400,
            detail="email or password incorrect"
        )
        
    access , refresh = accessManager.create_user_tokens(user)
       
    return JwtTokenResponse(accessToken=access,refreshToken=refresh)

@router.post(
    path="/register/",
    response_model=JwtTokenResponse,
    status_code=201,
)
def register_user(data : RegisterUserSchema ,repository : Repository , accessManager : JwtAccessServiceDep , hash :BcryptHashDep):
    exists_user_with_email = repository.get_by_email(data.email)
    
    if(exists_user_with_email):
        raise HTTPException(
            status_code=400,
            detail="An user with that email already exists"
        )
    
    data_dict = data.model_dump()
    password = hash.encrypt(data_dict.pop("password"))
    user = repository.create(User(**data_dict , password=password))
    access , refresh = accessManager.create_user_tokens(user)
    
    return JwtTokenResponse(accessToken=access,refreshToken=refresh)

@router.post(
    path="/token/verify/",
    status_code=204,
    tags=["token"]
)
def verify_token(data : VerifyTokenSchema , accessManager : JwtAccessServiceDep):
    if(not accessManager.verify_token(data.token)):
        raise HTTPException(status_code=401,detail="not authorization")

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