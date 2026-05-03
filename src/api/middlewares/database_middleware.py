from types import FunctionType
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from api.configs.db import get_session

class DbCommitMiddleware(
    BaseHTTPMiddleware
):
    async def dispatch(self,request: Request, call_next : FunctionType):
        response = None
        with get_session() as session:
            request.state.db = session
            try:
                response = await call_next(request)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        return response
