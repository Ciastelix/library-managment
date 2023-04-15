from app.models import Book
from app.repositories.book import BookRepository
from app.schemas import BookSchemaIn


class BookService:
    def __init__(self, book_repository: BookRepository) -> None:
        self._repository: BookRepository = book_repository

    def get_book(self, id: int = None, name: str = None) -> list[Book]:
        if id:
            return self._repository.get_by_id(id)
        elif name:
            return self._repository.get_by_name(name)
        else:
            return self._repository.get_all()

    def create_book(self, book: BookSchemaIn) -> Book:
        return self._repository.add(book)

    def delete_book(self, id: int) -> Book:
        return self._repository.delete(id)

    def update_book(self, id: int, book: BookSchemaIn) -> Book:
        return self._repository.update(id, book)
