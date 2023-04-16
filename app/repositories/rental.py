from .db_session_handler import add_to_db
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from app.models import Rental
from app.schemas import RentalSchemaIn
from sqlalchemy.orm import subqueryload


class RentalRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def add(self, rental: RentalSchemaIn) -> Rental:
        with self.session_factory() as session:
            rental = Rental(**rental.dict(exclude_unset=True))
            add_to_db(session, rental)
            return rental

    def get_by_user(self, user: str) -> Rental | list[Rental]:
        with self.session_factory() as session:
            return session.query(Rental).filter(Rental.user_id == user).all()

    def get_by_id(self, id: int) -> Rental:
        with self.session_factory() as session:
            return session.query(Rental).filter(Rental.id == id).first()

    def get_all(self) -> list[Rental]:
        with self.session_factory() as session:
            return session.query(Rental).all()

    def delete(self, id: int) -> Rental:
        with self.session_factory() as session:
            return session.query(Rental).filter(Rental.id == id).first().delete()

    def update(self, id: int, rental: RentalSchemaIn) -> Rental:
        with self.session_factory() as session:
            return (
                session.query(Rental)
                .filter(Rental.id == id)
                .update(rental.dict(exclude_unset=True))
            )
