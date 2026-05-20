from sqlmodel import Session

from api.configs.db import get_engine
from api.depends.auth_dep import get_bcrypt_hash
from api.models import User

with Session(get_engine()) as session:
    hash = get_bcrypt_hash()
    
    name = input("escreva seu nome ")
    email = input("escreva seu email ")
    password = input("escreva sua senha ")
    
    user = User(name=name , email=email , password=hash.encrypt(password) , is_staff=True)
    
    session.add(user)
    session.commit()
    
    print("admin criado")