from sqlmodel import Session , SQLModel , create_engine

from api.configs.settings import settings
from api.models import auth

def get_engine():
    return create_engine(settings.DATABASE_URL)

def get_session():
    return Session(get_engine())

def create_all_tables():
    SQLModel().metadata.create_all(get_engine())
