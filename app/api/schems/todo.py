from pydantic import BaseModel

from app.dto import Status


class Todo(BaseModel):

    name: str
    description: str | None
    status: Status


class EditTodo(BaseModel):

    todo_id: int
    name: str
    description: str | None
    status: Status


class DeleteTodo(BaseModel):

    todo_id: int
