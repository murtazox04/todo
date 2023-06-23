from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    def __str__(self):
        return f"{self.name}\n{self.email}\n{self.password}"
