from fastapi import APIRouter , HTTPException , UploadFile , File , Form
from uuid import uuid4

from api.shemas.input.auth_input import LoginUserSchema , RegisterUserSchema , UpdateUserSchema , VerifyTokenSchema , EmailUserSchema , PasswordUserSchema
from api.shemas.output.auth_output import JwtTokenResponse , UserDetailReponse
from api.shemas.output.general_output import DetailResponse , TokenResponse
from api.models.auth import User
from api.tasks import send_reset_password_email

from api.depends.auth_dep import UserRepositoryDep as RepositoryDep , JwtAccessServiceDep ,BcryptHashDep , RedisTokenServiceDep , UserDep
from api.core.files import save_file

router = APIRouter()

@router.post(
    path="/login/",
    tags=["auth"],
    response_model=JwtTokenResponse
)
def login_user(data : LoginUserSchema , repository : RepositoryDep , accessManager : JwtAccessServiceDep , hash :BcryptHashDep): 
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
    tags=["auth"],
    response_model=JwtTokenResponse,
    status_code=201,
)
def register_user(data : RegisterUserSchema ,repository : RepositoryDep , accessManager : JwtAccessServiceDep , hash :BcryptHashDep):
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
    tags=["auth"],
    status_code=200,
    response_model=DetailResponse
)
def get_reset_password_token(data : EmailUserSchema , repository : RepositoryDep , store : RedisTokenServiceDep):
    user = repository.get_by_email(data.email)
    
    if(user is None):
        raise HTTPException(
            status_code=400,
            detail="there is not any user with that email"
        )
    
    token = uuid4().hex
    store.store_reset_pass_token(token , user.id)
    send_reset_password_email.delay(str(user.email),token)
    return DetailResponse(detail="Email sended")

@router.post(
    path="/reset-password/{token}/",
    tags=["auth"],
    response_model=DetailResponse,
)
def reset_password(token : str , data : PasswordUserSchema , store : RedisTokenServiceDep , repostory : RepositoryDep , hash : BcryptHashDep):
    user_id = store.get_user_id_by_reset_pass_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="invalid token"
        )
        
    user = repostory.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=500,
            detail="err internal"
        )
        
    user.password = hash.encrypt(data.password)
    repostory.update(user)
    store.delete_reset_pass_token(token)
    return DetailResponse(detail="password updated")

@router.post(
    "/logout/",
    tags=["auth"],
    status_code=204
)
def logout_user():
    pass

@router.get(
    path="/me/",
    tags=["user"],
    response_model=UserDetailReponse
)
def get_mine_account(user : UserDep):
    return UserDetailReponse(**user.model_dump())

@router.patch(
    path="/me/",
    tags=["user"],
    response_model=UserDetailReponse,
)
def update_mine_account(user : UserDep , repository : RepositoryDep, name : str | None = Form(None) ,photo : UploadFile | None = File(None)):
    data = {}
    if photo:
        data["photo_url"] = save_file(photo,"users/photo/")
    if name:
        data["name"] = name
    
    for key , value in data.items() : setattr(user , key , value)
    repository.update(user)
    return UserDetailReponse(**user.model_dump())

@router.delete(
    path="/me/",
    tags=["user"],
    status_code=204
)
def delete_mine_account(user : UserDep , repository : RepositoryDep):
    repository.delete(user)

@router.post(
    path="/me/change-password/",
    tags=["user"],
    status_code=204
)
def change_password(user : UserDep , repository : RepositoryDep , hash : BcryptHashDep , data : PasswordUserSchema):
    user.password = hash.encrypt(data.password)
    repository.update(user)