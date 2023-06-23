from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app import dto

from app.infrastructure.database.dao.rdb.base import BaseDAO
from app.infrastructure.database.models.user import User


class UserDAO(BaseDAO[User]):
    def __int__(self, session: AsyncSession):
        super().__init__(User, session)

    async def add_user(self, name: str, email: str, password: str) -> dto.User:
        result = await self.session.execute(
            insert(User).values(
                name=name,
                email=email,
                password=password
            ).returning(User)
        )
        return dto.User.from_orm(result.scalar())
    
    
