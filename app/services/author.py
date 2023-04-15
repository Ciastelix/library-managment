from app.models import Author
from app.repositories.author import AuthorRepository
from app.schemas import AuthorSchemaIn


class AuthorService:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._repository: AuthorRepository = author_repository

    def get_author(self, id: int = None, name: str = None) -> list[Author]:
        if id:
            return self._repository.get_by_id(id)
        elif name:
            return self._repository.get_by_name(name)
        else:
            return self._repository.get_all()

    def create_author(self, author: AuthorSchemaIn) -> Author:
        return self._repository.add(author)

    def delete_author(self, id: int) -> Author:
        return self._repository.delete(id)

    def update_author(self, id: int, author: AuthorSchemaIn) -> Author:
        return self._repository.update(id, author)
