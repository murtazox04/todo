from app.dto import Base


class User(Base):

    name: str
    email: str


class UserWithPassword(Base):

    name: str
    email: str
    password: str
