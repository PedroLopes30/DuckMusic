from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from api.repository import UserRepository

from api.core.utils import BcryptHash
from api.depends.auth_dep import get_jwt_service
jwt_service = get_jwt_service()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        repository = UserRepository(request.state.db)
        email = form.get("username")
        password = form.get("password")

        user = repository.get_by_email(email)
        
        if user is None or not BcryptHash().verify(user.password , password):
            return False
        if not user.is_staff:
            return False
        access , refresh = jwt_service.create_user_tokens(user)
        request.session.update({"token": access})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token or not jwt_service.verify_token(token):
            return False

        
        return True


authentication_backend = AdminAuth(secret_key="...")