from jwt import encode , decode
from bcrypt import checkpw , gensalt , hashpw
from datetime import timedelta , datetime , timezone
import smtplib
from ssl import create_default_context
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import EmailStr
from redis import Redis

from api.interfaces import IAccessService , IHash , ITokensService
from api.models.auth import User

class JwtService(
    IAccessService
):
    def __init__(self,secret_key : str , algorithm , access_token_life_time : timedelta , refresh_token_life_time : timedelta):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_life_time = access_token_life_time
        self.refresh_token_life_time = refresh_token_life_time
    
    def create_user_tokens(self , user : User)->tuple[str,str]:
        now = datetime.now(timezone.utc)
        
        access_payload = self.get_access_token_payload(user , now) 
        
        refresh_content = self.get_refresh_token_payload(user , now)
        
        access_token = encode(access_payload , self.secret_key , algorithm=self.algorithm)
        refresh_token = encode(refresh_content , self.secret_key , algorithm=self.algorithm)
        return access_token, refresh_token
    
    def verify_token(self , token : str) -> bool:
        try:
            decode(token , self.secret_key , self.algorithm, options={"verify_exp": True})
            return True
        except:
            return False

    def get_access_token_payload(self , user : User , now : datetime)->dict:
        return {
            "user_id" : user.id,
            "username" : user.name,
            "iat" : now,
            "exp" : now + self.access_token_life_time
        }
    
    def get_refresh_token_payload(self , user : User , now : datetime)->dict:
        return  {
            "user_id": user.id , 
            "exp": now + self.refresh_token_life_time,
            "iat" : now , 
            "type" : "refresh"
        }
        
class BcryptHash(IHash):
    
    def encrypt(self, value):
        return hashpw(
            value.encode("utf8"),
            gensalt(10)
        ).decode("utf8")
        
    def verify(self, value, verify_value):
        return checkpw(
            verify_value.encode("utf8"),
            value.encode("utf8"),
        )

class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = password

    def _send(self, to_email: str, subject: str, html_content: str):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))
        
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False


    async def send_welcome_email(self, to_email: EmailStr, username: str):
        subject = "Bem-vindo ao nosso sistema!"
        html = f"""
        <html>
            <body>
                <h1>Olá, {username}!</h1>
                <p>Sua conta foi criada com sucesso. Aproveite o painel!</p>
            </body>
        </html>
        """
        return self._send(to_email, subject, html)

    async def send_password_reset(self, to_email: EmailStr, token: str, url  : str = "http://localhost:8000"):
        subject = "Recuperação de Senha"
        link = f"{url}/reset-password/{token}"
        html = f"<p>Clique no link para resetar sua senha: <a href='{link}'>Resetar Senha</a></p>"
        return self._send(to_email, subject, html)
    
class TokensService(ITokensService):
    def __init__(self , store : Redis):
        self.store = store
        
    def store_reset_pass_token(self, token , user_id)->None:
        user_token = self.get_user_reset_pass_by_index(user_id)
        
        if(user_token):
            self.delete_reset_pass_token(user_token)
            self.delete_user_reset_pass_index(user_id)
        
        self.add_token(f"reset_pass_{token}",str(user_id) , int(timedelta(minutes=30).total_seconds()))
        self.add_token(f"reset_pass_index_{user_id}",token , int(timedelta(minutes=30).total_seconds()))
    
    def get_user_id_by_reset_pass_token(self,token : str)->int:
        return self.get(f"reset_pass_{token}")
    
    def delete_user_reset_pass_index(self , user_id : int)->None:
        return self.delete_token(f"reset_pass_index_{user_id}")
    
    def delete_reset_pass_token(self, token):
        return self.delete_token(f"reset_pass_{token}")
    
    def get_user_reset_pass_by_index(self , user_id)->str | None:
        return self.get(f"reset_pass_index_{user_id}")
    
    def delete_token(self , token : str)->None:
        self.store.delete(token)
    
    def add_token(self , token : str , value : str , ttl : int)->None:
        self.store.set(token , value , ttl)
        
    def get(self, name : str)->str:
        return self.store.get(name)