from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column


from .base import BaseModel
from app import dto


class Todo(BaseModel):
    __tablename__ = 'todo'

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(Enum(dto.Status), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return f"{self.name}\n{self.description}\n{self.status}\n{self.user_id}"
