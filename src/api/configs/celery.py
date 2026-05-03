from celery import Celery

from api.configs.settings import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["api.tasks"]
)

celery_app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    celery_app.start()