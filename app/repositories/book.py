from .db_session_handler import add_to_db
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from app.models import Book
from app.schemas import BookSchemaIn
from sqlalchemy.orm import subqueryload


class BookRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def add(self, book: BookSchemaIn) -> Book:
        with self.session_factory() as session:
            book = Book(**book.dict(exclude_unset=True))
            add_to_db(session, book)
            return book

    def get_by_name(self, name: str) -> Book | list[Book]:
        with self.session() as session:
            return session.query(Book).filter(Book.name == name).all()

    def get_by_id(self, id: int) -> Book:
        with self.session() as session:
            return session.query(Book).filter(Book.id == id).first()

    def get_all(self) -> list[Book]:
        with self.session_factory() as session:
            return session.query(Book).options(subqueryload(Book.author)).all()

    def delete(self, id: int) -> Book:
        with self.session_factory() as session:
            return session.query(Book).filter(Book.id == id).first().delete()

    def update(self, id: int, book: BookSchemaIn) -> Book:
        with self.session_factory() as session:
            return (
                session.query(Book)
                .filter(Book.id == id)
                .update(book.dict(exclude_unset=True))
            )
