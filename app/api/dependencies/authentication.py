from datetime import timedelta
import datetime

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from passlib.context import CryptContext
import pytz
from app import dto

from app.config import Settings
from .database import dao_provider
from app.infrastructure.database.dao.holder import HolderDao


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_user(token: str = Depends(oauth2_scheme)) -> dto.User:
    ...


class AuthProvider:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.api.api_secret
        self.algorythm = "HS256"
        self.access_token_expire = timedelta(days=3)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(
            plain_password,
            hashed_password
        )

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta
    ) -> dto.Token:
        to_encode = data.copy()
        expire = datetime.datetime.now(
            tz=pytz.timezone('Asia/Tashkent')) + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorythm
        )
        return dto.Token(
            access_token=encoded_jwt,
            token_type="bearer"
        )

    def create_user_token(self, user: dto.User) -> dto.Token:
        return self.create_access_token(
            data={
                "sub": user.email
            },
            expires_delta=self.access_token_expire
        )

    async def authenticate_user(self, email: str, password: str, dao: HolderDao) -> dto.User:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        user = await dao.user.get_user_with_password(email=email)
        if user is None:
            raise http_status_401
        if self.verify_password(password, user.password):
            raise http_status_401
        return user

    async def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        dao: HolderDao = Depends(dao_provider)
    ) -> dto.User:
        credentials_exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=self.algorythm
            )
            email: str = payload.get("email")
            if email is None:
                raise credentials_exeption
        except JWTError:
            raise credentials_exeption

        user = await dao.user.get_user(email=email)
        if user is None:
            raise credentials_exeption
        return user
