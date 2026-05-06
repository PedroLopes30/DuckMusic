from fastapi import Depends , Header , HTTPException
from typing import Annotated
from datetime import timedelta

from api.configs.settings import settings

from api.interfaces import IUserRepository , IHash , IAccessService , ITokensService
from api.repository import UserRepository
from api.core.utils import JwtService , BcryptHash ,TokensService
from api.depends.data_dep import SessionDep , RedisDep

from api.models.auth import User

def get_user_repository(sessoin : SessionDep)->IUserRepository:
    return UserRepository(sessoin)

UserRepositoryDep = Annotated[IUserRepository , Depends(get_user_repository)]

def get_jwt_service()->IAccessService:
    return JwtService(
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM ,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), 
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
JwtAccessServiceDep = Annotated[IAccessService , Depends(get_jwt_service)]

def get_bcrypt_hash()->IHash:
    return BcryptHash()

BcryptHashDep = Annotated[IHash , Depends(get_bcrypt_hash)]

def get_token_service(store : RedisDep)->ITokensService:
    return TokensService(store)

RedisTokenServiceDep = Annotated[ITokensService , Depends(get_token_service)]

def get_user_id(accessToken : Annotated[str , Header()] , accessService : JwtAccessServiceDep)->int:
    if(not accessService.verify_token(accessToken)):
        raise HTTPException(
            status_code=401,
            detail="unauthorize"
        )
        
    return accessService.decode(accessToken).get("user_id")

UserIdDep = Annotated[int , Depends(get_user_id)]

def get_user(user_id : UserIdDep , repository : UserRepositoryDep)->User:
    user = repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="not found")
    
    return user

UserDep = Annotated[User,Depends(get_user)]