from fastapi import Depends , Request
from typing import Annotated
from sqlmodel import Session

def get_session(request : Request)->Session:
    return request.state.db

SessionDep = Annotated[Session , Depends(get_session)]