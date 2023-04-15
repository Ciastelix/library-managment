from contextlib import AbstractContextManager
from typing import Callable
from .db_session_handler import add_to_db
from sqlalchemy.orm import Session
from app.schemas import LibrarySchemaIn
from app.models import Library


class LibraryRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> list[Library]:
        with self.session_factory() as session:
            return session.query(Library).all()

    def get_by_id(self, id: int) -> Library:
        with self.session_factory() as session:
            return session.query(Library).filter(Library.id == id).first()

    def get_by_name(self, name: str) -> Library:
        with self.session_factory() as session:
            return session.query(Library).filter(Library.name == name).first()

    def add(self, library: LibrarySchemaIn) -> Library:
        with self.session_factory() as session:
            library = Library(**library.dict(exclude_unset=True))
            add_to_db(session, library)
            return library

    def delete(self, id: int) -> Library:
        with self.session_factory() as session:
            return session.query(Library).filter(Library.id == id).first().delete()

    def update(self, id: int, library: LibrarySchemaIn) -> Library:
        with self.session_factory() as session:
            return (
                session.query(Library)
                .filter(Library.id == id)
                .update(library.dict(exclude_unset=True))
            )
