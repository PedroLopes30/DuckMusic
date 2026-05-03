from pathlib import Path
from os.path import join
from pydantic_settings import BaseSettings , SettingsConfigDict
from typing import Optional

#path
BASE_DIR = Path(__file__).parent.parent.parent.parent
DOT_ENV_FILE_PATH = join(BASE_DIR , ".env")

#configs
class Settings(BaseSettings):
    #general
    DEBUG : bool = False
    SERVER_URL : str
    
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASS: Optional[str] = None
    
    # Email / Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None
    SMTP_SENDER : str
    SMTP_PORT : int = 465

    model_config = SettingsConfigDict(env_file=DOT_ENV_FILE_PATH)

settings = Settings()