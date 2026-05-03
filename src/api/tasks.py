from asyncio import run

from api.configs.celery import celery_app
from api.configs.settings import settings

from api.core.utils import EmailService

email_service = EmailService(
    password=settings.SMTP_PASS,
    sender_email=settings.SMTP_SENDER,
    smtp_port=settings.SMTP_PORT,
    smtp_server=settings.SMTP_HOST  
)

@celery_app.task
def send_reset_password_email(email: str, token: str):
    async def _send():
        if settings.DEBUG:
            print(
                f"email enviado para {email} com o token: {token} "
                f"para a url 'http://localhost:8000/reset-password/{token}'"
            )
        else:
            try:
                await email_service.send_password_reset(
                    to_email=email,
                    token=token,
                    url=settings.SERVER_URL
                )
                return True
            except Exception as e:
                print(e)
                return False
        

    return run(_send())
