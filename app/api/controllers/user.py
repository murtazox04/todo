from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import dto
from app.api import schems
from app.api.dependencies.authentication import AuthProvider
from app.api.dependencies.database import dao_provider
from app.api.dependencies.settings import get_settings
from app.config import Settings

from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter(prefix="/user")


@router.post(
    path="/login",
    description="Login user",
    response_model=dto.Token
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        dao: HolderDao = Depends(dao_provider),
        settings: Settings = Depends(get_settings)
):
    auth = AuthProvider(settings=settings)
    user = await auth.authenticate_user(
        email=form_data.username,
        password=form_data.password,
        dao=dao
    )
    token = auth.create_user_token(user=user)
    return token


@router.post(
    path="/register",
    description="Register new user"
)
async def create_user(
    user: schems.User,
    dao: HolderDao = Depends(dao_provider),
    settings: Settings = Depends(get_settings)
):
    auth = AuthProvider(settings=settings)
    if await dao.user.get_user(email=user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )
    return await dao.user.add_user(
        name=user.name,
        email=user.email,
        password=auth.get_password_hash(password=user.password)
    )
