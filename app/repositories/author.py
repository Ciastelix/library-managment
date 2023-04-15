from contextlib import AbstractContextManager
from typing import Callable
from .db_session_handler import add_to_db
from sqlalchemy.orm import Session
from app.models import Author
from app.schemas import AuthorSchemaIn
from sqlalchemy.orm import subqueryload


class AuthorRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> list[Author]:
        with self.session_factory() as session:
            return session.query(Author).options(subqueryload(Author.books)).all()

    def get_by_id(self, id: int) -> Author:
        with self.session_factory() as session:
            return (
                session.query(Author)
                .options(subqueryload(Author.books))
                .filter_by(id=id)
                .first()
            )

    def get_by_name(self, name: str) -> Author:
        with self.session_factory() as session:
            return session.query(Author).filter(Author.name == name).first()

    def add(self, author: AuthorSchemaIn) -> Author:
        with self.session_factory() as session:
            author = Author(**author.dict(exclude_unset=True))
            add_to_db(session, author)
            return author

    def delete(self, id: int) -> Author:
        with self.session_factory() as session:
            return session.query(Author).filter(Author.id == id).first().delete()

    def update(self, id: int, author: AuthorSchemaIn) -> Author:
        with self.session_factory() as session:
            return (
                session.query(Author)
                .filter(Author.id == id)
                .update(author.dict(exclude_unset=True))
            )
