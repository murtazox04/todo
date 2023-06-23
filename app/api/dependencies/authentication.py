from datetime import timedelta
from passlib.context import CryptContext

from app.config import Settings


class AuthProvider:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.api.api_secret
        self.algorythm = "HS256"
        self.access_token_expire = timedelta(days=3)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(
            plain_password,
            hashed_password
        )

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
