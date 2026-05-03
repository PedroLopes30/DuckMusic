from fastapi import Depends
from typing import Annotated
from datetime import timedelta

from api.configs.settings import settings

from api.interfaces import IUserRepository , IHash , IAccessService
from api.repository import UserRepository
from api.core.utils import JwtService , BcryptHash
from api.depends.db_dep import SessionDep

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