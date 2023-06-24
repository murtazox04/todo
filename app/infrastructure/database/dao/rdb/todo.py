from pydantic import parse_obj_as
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app import dto

from app.infrastructure.database.dao.rdb.base import BaseDAO
from app.infrastructure.database.models import Todo


class TodoDAO(BaseDAO[Todo]):
    def __init__(self, session: AsyncSession):
        super().__init__(Todo, session)

    async def add_todo(
        self,
        name: str,
        description: str | None,
        status: dto.Status,
        user_id: int
    ) -> dto.Todo:
        result = await self.session.execute(
            insert(Todo).values(
                name=name,
                description=description,
                status=status,
                user_id=user_id
            ).returning(Todo)
        )
        await self.session.commit()
        return dto.Todo.from_orm(result.scalar())

    async def get_todos(self, user_id: int) -> list[dto.Todo]:
        result = await self.session.execute(
            select(Todo).filter(Todo.user_id == user_id)
        )
        return parse_obj_as(list[dto.Todo], result.scalar().all())

    async def get_todo(self, user_id: int, todo_id: int) -> dto.Todo:
        result = await self.session.execute(
            select(Todo).filter(Todo.user_id == user_id, Todo.id == todo_id)
        )
        todo = result.scalar()
        if todo is not None:
            return dto.Todo.from_orm(todo)

    async def get_todo_by_name(self, user_id: int, name: str) -> dto.Todo:
        result = await self.session.execute(
            select(Todo).filter(Todo.user_id == user_id, Todo.name == name)
        )
        todo = result.scalar()
        if todo is not None:
            return dto.Todo.from_orm(todo)

    async def edit_todo(
        self,
        todo_id: int,
        name: str,
        description: str,
        status: dto.Status
    ) -> dto.Todo:
        result = await self.session.execute(
            update(Todo).values(
                name=name,
                description=description,
                status=status
            ).filter(Todo.id == todo_id).returning(Todo)
        )
        await self.session.commit()
        return dto.Todo.from_orm(result.scalar())
