from redis import Redis

from api.configs.settings import settings

def get_redis()->Redis:
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASS,
        db=settings.REDIS_DB,
        decode_responses=True
    )