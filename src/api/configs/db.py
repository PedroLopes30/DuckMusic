from sqlmodel import Session , SQLModel , create_engine

from api.configs.settings import Settings

def get_engine():
    return create_engine(Settings.DATABASE_URL)

def get_session():
    return Session(get_engine())

def create_all_tables():
    SQLModel().metadata.create_all(get_engine())
