from fastapi import Depends , Request
from typing import Annotated
from sqlmodel import Session
from redis import Redis

from api.configs.redis import get_redis

def get_session(request : Request)->Session:
    return request.state.db

SessionDep = Annotated[Session , Depends(get_session)]
RedisDep = Annotated[Redis , Depends(get_redis)]