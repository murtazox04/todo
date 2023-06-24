from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies.authentication import get_user
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao.holder import HolderDao


router = APIRouter(prefix="/todo")


@router.get(
    path="/all",
    description="Get all todos"
)
async def get_todos(
    user: dto.User = Depends(get_user),
    dao: HolderDao = Depends(dao_provider)
) -> list[dto.Todo]:
    return await dao.todo.get_todos(user_id=user.id)


@router.post(
    path="/new",
    description="Create new TODO"
)
async def new_todo(
    todo: schems.Todo,
    user: dto.User = Depends(get_user),
    dao: HolderDao = Depends(dao_provider)
) -> dto.Todo:
    if await dao.todo.get_todo_by_name(user_id=user.id, name=todo.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo already created"
        )
    return await dao.todo.add_todo(
        name=todo.name,
        description=todo.description,
        status=todo.status,
        user_id=user.id
    )


@router.put(
    path="/edit",
    description="Edit existing TODO"
)
async def edit_todo(
    todo: schems.EditTodo,
    user: dto.User = Depends(get_user),
    dao: HolderDao = Depends(dao_provider)
) -> dto.Todo:
    if await dao.todo.get_todo(user_id=user.id, todo_id=todo.todo_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo not found"
        )
    return await dao.todo.edit_todo(
        todo_id=todo.todo_id,
        name=todo.name,
        description=todo.description,
        status=todo.status
    )


@router.delete(
    path="/delete",
    description="Delete existing TODO"
)
async def delete_todo(
    todo: schems.DeleteTodo,
    user: dto.User = Depends(get_user),
    dao: HolderDao = Depends(dao_provider)
) -> dto.Todo:
    if await dao.todo.get_todo(user_id=user.id, todo_id=todo.todo_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo not found"
        )
    return await dao.todo.delete_todo(todo_id=todo.todo_id)
