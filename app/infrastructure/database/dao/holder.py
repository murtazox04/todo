from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dao.rdb import BaseDAO, UserDAO, TodoDAO


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.base = BaseDAO
        self.user = UserDAO(self.session)
        self.todo = TodoDAO(self.session)
