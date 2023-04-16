from sqlalchemy import Column, String, Date, ForeignKey, Boolean
from app.db import Base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime


class Author(Base):
    __tablename__ = "authors"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    books = relationship(
        "Book", back_populates="author", cascade="all, delete", lazy="joined"
    )

    def __repr__(self) -> str:
        return f"Author(name={self.name}"


class Book(Base):
    __tablename__ = "books"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    written_at = Column(Date, nullable=True)
    author_id = Column(String, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books", lazy="joined")
    library_id = Column(String, ForeignKey("libraries.id"))
    library = relationship("Library", back_populates="books", lazy="joined")
    rental = relationship("Rental", back_populates="book", uselist=False)

    def __repr__(self) -> str:
        return f"Book(name={self.name} written_at={self.written_at})"


class Library(Base):
    __tablename__ = "libraries"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    books = relationship(
        "Book", back_populates="library", cascade="all, delete", lazy="joined"
    )

    def __repr__(self) -> str:
        return f"Library(name={self.name}, city={self.city}, books={self.books})"


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True, unique=True)
    email = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    rentals = relationship("Rental", back_populates="user", lazy="joined")

    def __repr__(self) -> str:
        return f"User(name={self.name}, email={self.email}, password={self.password}, is_active={self.is_active}, is_superuser={self.is_superuser}, rentals={self.rentals})"


class Rental(Base):
    __tablename__ = "rentals"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    book_id = Column(String, ForeignKey("books.id"))
    book = relationship("Book", back_populates="rental", lazy="joined")
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="rentals", lazy="joined")
    rented_at = Column(Date, nullable=False, default=datetime.now().date())
    returned_at = Column(Date, nullable=True)

    def __repr__(self) -> str:
        return f"Rental(book_id={self.book_id}, user_id={self.user_id}, rented_at={self.rented_at}, returned_at={self.returned_at})"
