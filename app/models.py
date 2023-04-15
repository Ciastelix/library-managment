from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.db import Base
from sqlalchemy.orm import relationship
import uuid


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
