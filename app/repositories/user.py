from .db_session_handler import add_to_db
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserSchemaIn
from .password_managment import hash_password
from sqlalchemy.orm import subqueryload


class UserRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def add(self, user: UserSchemaIn) -> User:
        with self.session_factory() as session:
            user = User(**user.dict(exclude_unset=True))
            user.password = hash_password(user.password)
            add_to_db(session, user)
            return user

    def get_by_name(self, name: str) -> list[User]:
        with self.session_factory() as session:
            return session.query(User).filter(User.name == name).all()

    def get_by_email(self, email: str) -> list[User]:
        with self.session_factory() as session:
            return session.query(User).filter(User.email == email).all()

    def get_by_id(self, id: int) -> list[User]:
        with self.session_factory() as session:
            return session.query(User).filter(User.id == id).first()

    def get_all(self) -> list[User]:
        with self.session_factory() as session:
            return session.query(User).options(subqueryload(User.rentals)).all()

    def delete(self, id: int) -> User:
        with self.session_factory() as session:
            return session.query(User).filter(User.id == id).first().delete()

    def update(self, id: int, user: UserSchemaIn) -> User:
        with self.session_factory() as session:
            if user.password:
                user.password = User.hash_password(user.password)
            return (
                session.query(User)
                .filter(User.id == id)
                .update(user.dict(exclude_unset=True))
            )
