from app.dto import Base
from .types import Status


class Todo(Base):

    name: str
    description: str
    status: Status
