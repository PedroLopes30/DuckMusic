from sqladmin import ModelView

from api.models.auth import User
from api.depends.auth_dep import get_bcrypt_hash

hash = get_bcrypt_hash()

class UserAdmin(
    ModelView , model=User
):
    column_list = [User.id , User.name , User.email]
    
    def on_model_change(self, data, model, is_created, request):
        password = data.pop("password")
        data["password"] = hash.encrypt(password)
        return super().on_model_change(data, model, is_created, request)