from fastapi import APIRouter, Depends
from app.api.dependencies.database import dao_provider

from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter(prefix="/user")


@router.post(
    path="/login",
    description="Login user"
)
async def login(dao: HolderDao = Depends(dao_provider)):
    ...


@router.post(
    path="/register",
    description="Register new user"
)
async def create_user():
    ...
